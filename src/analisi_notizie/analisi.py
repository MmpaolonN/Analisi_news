"""Classificazione dei topic, sentiment analysis (VADER e RoBERTa) e validazione con LLM."""

from functools import lru_cache

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, classification_report
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from analisi_notizie.config import (
    BATCH_SIZE,
    CHUNK_SIZE,
    IPTC_MEDIA_TOPIC,
    IPTC_MEDIA_TOPIC_DESC,
    LLM_COMPARISONS,
    LLM_PROMPT,
    SENTIMENT_LABELS,
    SENTIMENT_MODEL,
)

# --- Topic: classificazione zero-shot con gli embedding ---


def classify(to_classify, classifier, labels=None):
    """
    Assegna ogni testo alla classe più simile (similarità coseno).

    Parameters:
    to_classify (np.ndarray): Embedding dei testi, forma (n_testi, dim).
    classifier (np.ndarray): Embedding delle classi, forma (n_classi, dim).
    labels (list, optional): Nomi delle classi, nello stesso ordine di classifier. Se None, restituisce gli indici.

    Returns:
    np.ndarray: Classe predetta per ogni testo.
    np.ndarray: Similarità con la classe predetta.
    np.ndarray: Matrice completa delle similarità, forma (n_testi, n_classi).
    """
    # array 2D di float, normalizzati così il prodotto scalare è la similarità coseno
    to_classify = np.atleast_2d(to_classify).astype(np.float32)
    classifier = np.atleast_2d(classifier).astype(np.float32)
    to_classify /= np.linalg.norm(to_classify, axis=1, keepdims=True)
    classifier /= np.linalg.norm(classifier, axis=1, keepdims=True)

    sims = to_classify @ classifier.T
    best = sims.argmax(axis=1)
    scores = sims[np.arange(len(best)), best]  # similarità della classe vincente

    if labels is not None:
        best = np.asarray(labels)[best]
    return best, scores, sims


# --- Sentiment 1: VADER ---


def label_sentiment(compound):
    """
    Trasforma il punteggio compound di VADER in un'etichetta (soglie standard di VADER).

    Parameters:
    compound (float): Punteggio compound di VADER, tra -1 e 1.

    Returns:
    str: "positive", "negative" o "neutral" (None se il punteggio manca).
    """
    if pd.isna(compound):
        return None
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    return "neutral"


# --- Sentiment 2: RoBERTa, su chunk di token ---


@lru_cache(maxsize=1)
def load_sentiment_model():
    """
    Carica tokenizer e modello una sola volta, al primo utilizzo.

    Returns:
    AutoTokenizer: Il tokenizer di SENTIMENT_MODEL.
    AutoModelForSequenceClassification: Il modello, in modalità predizione.
    """
    tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL).eval()
    return tokenizer, model


def df_to_token(df, text_col="full_article", max_chunks=None):
    """
    Tokenizza ogni testo e lo divide in chunk da CHUNK_SIZE token.

    Parameters:
    df (pd.DataFrame): Il DataFrame con i testi.
    text_col (str): La colonna con i testi.
    max_chunks (int, optional): Tiene solo i primi max_chunks chunk di ogni testo (più veloce). Se None, tutti i chunk.

    Returns:
    list: [(indice della riga, chunk di token), ...]
    """
    tokenizer, _ = load_sentiment_model()
    records = []
    for row_id, text in df[text_col].fillna("").items():  # NaN -> "" così il tokenizer non dà errore
        ids = tokenizer(text, add_special_tokens=False)["input_ids"]
        ids = ids[: CHUNK_SIZE * max_chunks] if max_chunks else ids
        for i in range(0, len(ids), CHUNK_SIZE):
            records.append((row_id, ids[i : i + CHUNK_SIZE]))
    return records


@torch.no_grad()  # niente gradienti: servono solo per l'addestramento, qui sprecherebbero memoria
def chunk_prediction(records):
    """
    Predice il sentiment di ogni chunk, BATCH_SIZE chunk alla volta.

    Parameters:
    records (list): Output di df_to_token.

    Returns:
    list: [(indice della riga, n_token, probabilità delle classi), ...]
    """
    tokenizer, model = load_sentiment_model()
    records = sorted(records, key=lambda r: len(r[1]))  # chunk di lunghezza simile nello stesso batch: meno padding
    results = []
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i : i + BATCH_SIZE]
        inputs = [[tokenizer.cls_token_id] + tok + [tokenizer.sep_token_id] for _, tok in batch]  # aggiungo <s> e </s>
        encoded = tokenizer.pad({"input_ids": inputs}, return_tensors="pt")  # stessa lunghezza + attention_mask
        probs = torch.softmax(model(**encoded).logits, dim=-1)
        results += [(row_id, len(tok), p.tolist()) for (row_id, tok), p in zip(batch, probs)]
    return results


def aggregate_chunks(df, predictions):
    """
    Media delle probabilità dei chunk di ogni articolo, pesata per numero di token.

    Parameters:
    df (pd.DataFrame): Il DataFrame usato in df_to_token.
    predictions (list): Output di chunk_prediction.

    Returns:
    pd.DataFrame: df con una colonna per classe e una colonna "sentiment" (classe più probabile).
    """
    _, model = load_sentiment_model()
    labels = list(model.config.id2label.values())  # ['negative', 'neutral', 'positive']

    pred = pd.DataFrame([p for _, _, p in predictions], columns=labels)  # una riga per chunk
    ids = [row_id for row_id, _, _ in predictions]
    weights = pd.Series([n for _, n, _ in predictions])
    weighted_sum = pred.mul(weights, axis=0).groupby(ids).sum()  # somma(prob * token) per articolo
    mean = weighted_sum.div(weights.groupby(ids).sum(), axis=0)  # / token totali dell'articolo
    mean["sentiment"] = mean[labels].idxmax(axis=1)
    return df.join(mean)  # allineato sull'indice delle righe


# --- Validazione con LLM ---


def llm_prompt_files(df, out_dir, n=50, size=25, seed=42):
    """
    Estrae n articoli a caso e li scrive, con LLM_PROMPT in testa, in file da `size` articoli da incollare nella chat dell'LLM.

    Parameters:
    df (pd.DataFrame): Il DataFrame con "headline" e "full_article".
    out_dir (Path): Cartella dei file llm_prompt_1.txt, llm_prompt_2.txt, ...
    n (int): Numero di articoli.
    size (int): Articoli per file (file più piccoli = risposte più affidabili).
    seed (int): Seed casuale, così il campione è sempre lo stesso.

    Returns:
    pd.DataFrame: Le righe estratte.
    """
    sample = df.sample(n=n, random_state=seed)
    # stesse descrizioni dei topic usate dagli embedding, così il confronto è equo
    topics = "\n".join(f"- {name}: {desc}" for name, desc in zip(IPTC_MEDIA_TOPIC, IPTC_MEDIA_TOPIC_DESC))
    for i, start in enumerate(range(0, n, size), start=1):
        block = sample.iloc[start : start + size]
        # ID = indice della riga nel df: serve per riattaccare le etichette alle righe giuste
        articles = "\n\n".join(f"### ID: {idx}\nTitolo: {r.headline}\nTesto: {r.full_article}" for idx, r in block.iterrows())
        text = LLM_PROMPT.format(topics=topics, n=len(block)) + "\n" + articles
        (out_dir / f"llm_prompt_{i}.txt").write_text(text, encoding="utf-8")
    return sample


def load_llm_labels(df, path, expected_ids):
    """
    Carica le risposte dell'LLM (CSV id;topic;sentiment), stampa eventuali errori e le aggiunge al df.

    Parameters:
    df (pd.DataFrame): Il DataFrame da cui è stato estratto il campione.
    path (Path): Il CSV con le risposte dell'LLM.
    expected_ids (Index): Gli ID del campione.

    Returns:
    pd.DataFrame: df con le colonne "llm_topic" e "llm_sentiment" (vuote fuori dal campione).
    """
    # separatore ";" perché "Guerra, conflitti e terrorismo" contiene una virgola
    llm = pd.read_csv(path, sep=";", index_col="id").apply(lambda col: col.str.strip())
    print("ID mancanti:", sorted(set(expected_ids) - set(llm.index)))
    print("ID in più:", sorted(set(llm.index) - set(expected_ids)), "duplicati:", llm.index[llm.index.duplicated()].tolist())
    print("Topic non validi:", llm.loc[~llm["topic"].isin(IPTC_MEDIA_TOPIC), "topic"].to_dict())
    print("Sentiment non validi:", llm.loc[~llm["sentiment"].isin(SENTIMENT_LABELS), "sentiment"].to_dict())

    llm = llm[~llm.index.duplicated()]  # un ID duplicato duplicherebbe la riga nel df
    df = df.drop(columns=["llm_topic", "llm_sentiment"], errors="ignore")  # così la funzione si può rieseguire
    return df.join(llm.rename(columns={"topic": "llm_topic", "sentiment": "llm_sentiment"}))


def llm_accuracy(df):
    """
    Stampa il classification report di ogni metodo di LLM_COMPARISONS, usando le etichette dell'LLM come riferimento.

    Parameters:
    df (pd.DataFrame): Output di load_llm_labels.

    Returns:
    pd.Series: Accuracy di ogni metodo.
    """
    val = df.dropna(subset=["llm_topic"])  # solo gli articoli etichettati
    accuracy = {}
    for name, ref_col, pred_col, _ in LLM_COMPARISONS:
        print(name, classification_report(val[ref_col], val[pred_col], zero_division=0), sep="\n")
        accuracy[name] = accuracy_score(val[ref_col], val[pred_col])
    return pd.Series(accuracy, name="accuracy").round(2)
