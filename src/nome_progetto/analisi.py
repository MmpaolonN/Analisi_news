from functools import lru_cache

import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from nome_progetto.config import BATCH_SIZE, CHUNK_SIZE, SENTIMENT_MODEL


def classify(to_classify, classifier, labels=None):
    """
    Assign each text to the most similar class (cosine similarity).

    Parameters:
    to_classify (np.ndarray): Text embeddings, shape (n_texts, dim).
    classifier (np.ndarray): Class embeddings, shape (n_classes, dim).
    labels (list, optional): Class names, same order as classifier. If None, indices are returned.

    Returns:
    np.ndarray: Predicted class of each text.
    np.ndarray: Similarity with the predicted class.
    np.ndarray: Full similarity matrix, shape (n_texts, n_classes).
    """
    # 2D float arrays, normalized so that the dot product is the cosine similarity
    to_classify = np.atleast_2d(to_classify).astype(np.float32)
    classifier = np.atleast_2d(classifier).astype(np.float32)
    to_classify /= np.linalg.norm(to_classify, axis=1, keepdims=True)
    classifier /= np.linalg.norm(classifier, axis=1, keepdims=True)

    sims = to_classify @ classifier.T
    best = sims.argmax(axis=1)
    scores = sims[np.arange(len(best)), best]  # similarity of the winning class

    if labels is not None:
        best = np.asarray(labels)[best]
    return best, scores, sims


def label_sentiment(compound):
    """
    Turn a VADER compound score into a label (standard VADER thresholds).

    Parameters:
    compound (float): VADER compound score, between -1 and 1.

    Returns:
    str: "positive", "negative" or "neutral" (None if the score is missing).
    """
    if pd.isna(compound):
        return None
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    return "neutral"


@lru_cache(maxsize=1)
def load_sentiment_model():
    """
    Load tokenizer and model only once, on first use.

    Returns:
    AutoTokenizer: The tokenizer of SENTIMENT_MODEL.
    AutoModelForSequenceClassification: The model, in prediction mode.
    """
    tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL).eval()
    return tokenizer, model


def df_to_token(df, text_col="full_article"):
    """
    Tokenize each text and split it into chunks of CHUNK_SIZE tokens.

    Parameters:
    df (pd.DataFrame): The DataFrame with the texts.
    text_col (str): The column with the texts.

    Returns:
    list: [(row index, token chunk), ...]
    """
    tokenizer, _ = load_sentiment_model()
    records = []
    for row_id, text in df[text_col].fillna("").items():  # NaN -> "" so the tokenizer does not fail
        ids = tokenizer(text, add_special_tokens=False)["input_ids"]
        for i in range(0, len(ids), CHUNK_SIZE):
            records.append((row_id, ids[i:i + CHUNK_SIZE]))
    return records


@torch.no_grad()  # no gradients: only needed for training, here they would waste memory
def chunk_prediction(records):
    """
    Predict the sentiment of each chunk, BATCH_SIZE chunks at a time.

    Parameters:
    records (list): Output of df_to_token.

    Returns:
    list: [(row index, n_tokens, class probabilities), ...]
    """
    tokenizer, model = load_sentiment_model()
    results = []
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        inputs = [[tokenizer.cls_token_id] + tok + [tokenizer.sep_token_id] for _, tok in batch]  # add <s> and </s>
        encoded = tokenizer.pad({"input_ids": inputs}, return_tensors="pt")             # same length + attention_mask
        probs = torch.softmax(model(**encoded).logits, dim=-1)
        results += [(row_id, len(tok), p.tolist()) for (row_id, tok), p in zip(batch, probs)]
    return results


def aggrega_chunk(df, predictions):
    """
    Average the chunk probabilities of each article, weighted by number of tokens.

    Parameters:
    df (pd.DataFrame): The DataFrame used in df_to_token.
    predictions (list): Output of chunk_prediction.

    Returns:
    pd.DataFrame: df with one column per class and a "sentiment" column (most likely class).
    """
    _, model = load_sentiment_model()
    labels = list(model.config.id2label.values())  # ['negative', 'neutral', 'positive']

    pred = pd.DataFrame([p for _, _, p in predictions], columns=labels)  # one row per chunk
    ids = [row_id for row_id, _, _ in predictions]
    weights = pd.Series([n for _, n, _ in predictions])
    weighted_sum = pred.mul(weights, axis=0).groupby(ids).sum()          # sum(prob * tokens) per article
    mean = weighted_sum.div(weights.groupby(ids).sum(), axis=0)          # / total tokens of the article
    mean["sentiment"] = mean[labels].idxmax(axis=1)
    return df.join(mean)  # aligned on the row index
