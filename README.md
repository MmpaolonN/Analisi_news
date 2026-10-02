# Analisi di notizie del New York Times: topic e sentiment

Progetto di NLP su un campione di ==***1000* articoli del New York Times del 1985**==. 
**l'obiettivo è rispondere a queste domande**:
- Con il passare degli anni si parla sempre delle stesse cose?
- Come cambia il tono in base all’argomento?

Per ogni articolo:
1. **classifico il topic** in una delle 13 categorie *IPTC Media Topics*, senza addestrare nessun modello (classificazione *zero-shot* con gli embedding);
2. **misuro il sentiment** con due metodi molto diversi, **VADER** (dizionario di parole) e **RoBERTa** (modello transformer);
3. **valido i risultati** confrontandoli con le etichette assegnate da un LLM a ==50== articoli, con confusion matrix e accuracy.

## Pipeline

| Fase         | Cosa faccio                                                                                                                        | Codice                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Esplorazione | Report interattivo con Sweetviz (colonne, valori mancanti, distribuzioni)                                                          | notebook, sezione 1                                           |
| Pulizia      | Tengo e rinomino 5 colonne (autore, data, sezione, titolo, testo), rimuovo articoli senza testo e duplicati                        | `cleaning.clean_news`                                         |
| Embedding    | Titolo + testo di ogni articolo  diventano vettori grazie a `all-MiniLM-L6-v2`                                                     | notebook, sezione 3                                           |
| Topic        | Ogni articolo va al topic con la descrizione più simile (similarità coseno)                                                        | `analisi.classify`                                            |
| Sentiment 1  | VADER: punteggio `compound` tra -1 e 1, soglie standard ±0.05                                                                      | `analisi.label_sentiment`                                     |
| Sentiment 2  | RoBERTa (`cardiffnlp/twitter-roberta-base-sentiment-latest`): testo diviso in chunk da 510 token, probabilità mediate per articolo | `analisi.df_to_token`, `chunk_prediction`, `aggregate_chunks` |
| Validazione  | ==50== articoli a caso etichettati da un LLM con le stesse definizioni, poi confusion matrix e accuracy                            | `analisi.llm_prompt_files`, `load_llm_labels`, `llm_accuracy` |

### Dettagli tecnici
- **RoBERTa più veloce su CPU**: i chunk vengono ordinati per lunghezza prima di formare i batch, così il padding è minimo (stessi risultati, 1.4× più veloce); con `max_chunks=1` si usa solo il primo chunk di ogni articolo (2.1× più veloce, 93% delle etichette invariate).
- **Validazione con LLM**: il prompt (in `config.py`) usa le stesse descrizioni dei topic degli embedding, e chiede un CSV separato da `;` con un ID per articolo, così le risposte si ricollegano alle righe giuste e vengono controllate (ID mancanti, etichette non valide).

## Risultati


## Struttura del progetto

```
├── notebooks/
│   └── analisi_notizie_nyt.ipynb   ← il notebook con tutta l'analisi, dall'esplorazione alle conclusioni
├── src/analisi_notizie/            ← il codice, richiamato dal notebook
│   ├── config.py                   ← percorsi, parametri, topic IPTC, prompt per l'LLM
│   ├── cleaning.py                 ← pulizia del dataset
│   ├── analisi.py                  ← topic, sentiment (VADER e RoBERTa), validazione con LLM
│   └── graphs.py                   ← grafici
├── scripts/
│   └── merge_full_text_csv.py      ← unisce i CSV originali del NYT (uno per anno) in un unico file
├── images/                         ← grafici usati in questo README
├── .data/                          ← dati (non su Git)
├── pyproject.toml                  ← dipendenze
└── uv.lock                         ← versioni esatte
```

## Come eseguirlo

Serve [uv](https://docs.astral.sh/uv/) e Python 3.13.

```powershell
uv sync                                   # crea .venv e installa dipendenze e pacchetto
```

1. Metti il dataset in `.data/NYT_sample.csv` (colonne usate: `writer_name`, `pub_date`, `section_name`, `main_headline`, `body_text`).
2. Apri `notebooks/analisi_notizie_nyt.ipynb` in VS Code e seleziona il kernel di `.venv`.
3. Esegui le celle in ordine. La cella di RoBERTa richiede circa 20 minuti su CPU.
4. Per la validazione: la cella della sezione 7 crea `.data/llm_prompt_1.txt` e `llm_prompt_2.txt`; incolla ciascuno in un LLM e salva le risposte in `.data/llm_labels.csv` (istruzioni nel notebook).

## Tecnologie
Python 3.13 · pandas · scikit-learn · sentence-transformers · transformers / PyTorch · vaderSentiment · matplotlib · plotly · Sweetviz · uv · ruff
