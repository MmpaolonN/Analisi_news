"""Grafici: embedding in 3D, quota dei topic, sentiment per topic e confusion matrix della validazione con LLM."""

import math

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from matplotlib.ticker import MaxNLocator
from sklearn.decomposition import PCA
from sklearn.metrics import ConfusionMatrixDisplay

from analisi_notizie.config import LLM_COMPARISONS

SENTIMENT_COLORS = {"negative": "red", "neutral": "white", "positive": "green"}  # ordine dal basso verso l'alto nelle aree


def embedding_to_3d(embeddings, labels=None):
    """Riduce gli embedding a 3 dimensioni con la PCA e li disegna nel browser come vettori che partono da 0, con l'etichetta sulla punta."""
    punti = PCA(n_components=3).fit_transform(embeddings)
    x, y, z = punti[:, 0], punti[:, 1], punti[:, 2]

    # Segmenti origine -> punto, separati da None per disegnarli in una sola traccia
    linee = [[c for v in coord for c in (0, v, None)] for coord in (x, y, z)]
    fig = go.Figure(go.Scatter3d(x=linee[0], y=linee[1], z=linee[2], mode="lines", line=dict(width=4), hoverinfo="skip"))
    # Punta della freccia: un cono orientato come il vettore
    fig.add_trace(go.Cone(x=x, y=y, z=z, u=x, v=y, w=z, anchor="tip", sizemode="absolute", sizeref=0.1, showscale=False, colorscale=[[0, "#636efa"], [1, "#636efa"]]))
    if labels is not None:
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="text", text=labels, textposition="top center"))
    fig.update_layout(showlegend=False)
    fig.show(renderer="browser")


def topic_share(df, topic_col="pred_topic", date_col="date"):
    """Grafico ad aree impilate 100% dei topic per anno (per mese se c'è un solo anno)."""
    period = _period(df[date_col])
    ax = pd.crosstab(period, df[topic_col], normalize="index").mul(100).plot.area(colormap="tab20", linewidth=0, ylabel="%", xlabel="")
    for area in ax.collections:  # bordo nero sottile per separare i topic
        area.set_edgecolor("black")
        area.set_linewidth(0.5)
    ax.set_ylim(0, 100)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1, 1))  # stesso ordine delle aree: in alto il topic in cima


def sentiment_by_topic(df, sentiment_col="sentiment_label", topic_col="pred_topic", date_col="date", ncols=4):
    """Un grafico ad aree impilate per topic: numero di articoli negativi, neutri e positivi per anno (per mese se c'è un solo anno)."""
    # tutti i periodi come righe, (topic, sentiment) come colonne: i periodi senza articoli valgono 0
    counts = pd.crosstab(_period(df[date_col]), [df[topic_col], df[sentiment_col]])
    topics = counts.columns.get_level_values(0).unique()

    nrows = math.ceil(len(topics) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows), sharex=True, squeeze=False)
    for ax, topic in zip(axes.flat, topics):
        # aree impilate dal basso: rosso, bianco, verde
        counts[topic].reindex(columns=list(SENTIMENT_COLORS), fill_value=0).plot.area(ax=ax, color=SENTIMENT_COLORS, linewidth=0, legend=False, title=topic, xlabel="", ylabel="n. articoli")
        for area in ax.collections:  # bordo nero, se no l'area bianca non si vede
            area.set_edgecolor("black")
            area.set_linewidth(0.8)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # niente mezzi articoli sull'asse
    for i in range(len(topics), axes.size):  # riquadri avanzati: li nascondo e sposto le date sul grafico sopra
        axes.flat[i].set_visible(False)
        axes.flat[i - ncols].tick_params(which="both", labelbottom=True)

    fig.legend(*axes.flat[0].get_legend_handles_labels(), loc="upper center", ncol=3)
    fig.tight_layout(rect=(0, 0, 1, 0.96))


def llm_confusion_matrices(df):
    """Una confusion matrix per ogni metodo di LLM_COMPARISONS: righe = etichetta dell'LLM, colonne = predizione del metodo."""
    val = df.dropna(subset=["llm_topic"])  # solo gli articoli etichettati
    for name, ref_col, pred_col, labels in LLM_COMPARISONS:
        size = max(4, len(labels) * 0.7)  # 13 topic: serve un grafico più grande
        _, ax = plt.subplots(figsize=(size, size))
        ConfusionMatrixDisplay.from_predictions(val[ref_col], val[pred_col], labels=labels, xticks_rotation=90, colorbar=False, ax=ax)
        ax.set(title=name, xlabel="Predetto", ylabel="Riferimento (LLM)")


def _period(dates):
    """Anno se le date coprono più anni, altrimenti mese."""
    date = pd.to_datetime(dates, dayfirst=True)
    return date.dt.year if date.dt.year.nunique() > 1 else date.dt.to_period("M")
