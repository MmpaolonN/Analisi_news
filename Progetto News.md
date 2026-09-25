#### Giorno 1 — Fondamenta + scoping

**Obiettivo**: colmare i buchi di Python essenziali e chiudere le decisioni di scope.

- Concetti Python da rivedere (solo l'essenziale, non un corso completo): liste/dict, loop, funzioni, `pandas` (DataFrame, filtri, groupby, merge), leggere/scrivere CSV
- Risorsa veloce: un crash course pandas di 2-3 ore è sufficiente (es. i notebook ufficiali di pandas o Kaggle Learn "Pandas")
- Decidi: 2-3 testate, periodo (consiglio 5-8 anni, non di più — più anni = più rumore da gestire), fonte dati (dataset esistente vs scraping leggero)
- Setup: Google Colab, repo GitHub vuoto con README iniziale
- **Output di giornata**: dataset grezzo (anche solo 500-1000 articoli per iniziare) con colonne minime: data, testata, autore (se disponibile), titolo, testo, categoria/sezione

⚠️ Attenzione fin da subito: verifica se le testate scelte **mostrano l'autore** in modo consistente — è un requisito hard per le domande su "giornalista". Se non c'è, quella domanda va tagliata subito, non a metà settimana.

#### Giorno 2 — Pulizia dati + EDA base (tema 1: distribuzione temi)

- Concetti: text cleaning (lowercase, rimozione punteggiatura/stopword), tokenizzazione
- Strumenti: `spaCy` con modello italiano (`it_core_news_sm`) oppure semplicemente `nltk` per stopword italiane
- Per "distribuzione dei temi nel tempo": se il sito ha già categorie/sezioni (politica, cronaca, ambiente...), usale come proxy diretto — è molto più veloce e affidabile di un topic modeling non supervisionato. Se non le ha, prova **BERTopic** (più semplice da usare bene rispetto a LDA classico, richiede meno tuning)
- **Output**: grafico distribuzione % articoli per tema per anno (già rispondi alla prima domanda)

#### Giorno 3 — Tono per tema (sentiment)

- Concetti: sentiment analysis, differenza tra sentiment a livello documento vs a livello di entità (aspect-based) — per ora fai document-level, è più fattibile
- Strumenti: per l'italiano, `feel-it` (libreria pip, modello pre-addestrato specifico per sentiment in italiano) è la scelta più pratica — non serve addestrare nulla
- Applica il modello a ogni articolo, aggrega per tema/anno
- **Output**: grafico tono medio per tema nel tempo (seconda domanda risolta)

#### Giorno 4 — Partiti/leader + dati esterni (terza domanda core)

- Concetti: named entity recognition (NER) per identificare menzioni di partiti/leader, oppure — più semplice e affidabile con poco tempo — matching per keyword/alias (liste di nomi partiti e leader)
- Sentiment positivo/negativo sulle frasi/paragrafi che menzionano l'entità (non sull'intero articolo, altrimenti il segnale si diluisce)
- Dati esterni: cerca serie storiche di sondaggi elettorali italiani (es. aggregatori come Termometro Politico, o dataset Wikipedia/Wikidata sui sondaggi) — anche pochi punti temporali bastano per un confronto visivo
- **Output**: grafico menzioni + sentiment per partito/leader sovrapposto a curva di popolarità reale

**Checkpoint metà settimana**: a questo punto hai le 3 domande core risolte. Da qui, procedi agli stretch SOLO se sei in linea con i tempi.

#### Giorno 5 (se in anticipo) — Predizione giornalista

- Concetti: train/test split, vettorizzazione testo (**TF-IDF**, più semplice di embedding neurali per iniziare), classificazione (Naive Bayes o Logistic Regression — non serve nulla di più complesso)
- Strumenti: `scikit-learn` (`TfidfVectorizer`, `train_test_split`, `MultinomialNB` o `LogisticRegression`)
- Valuta con accuracy + confusion matrix (quali giornalisti vengono confusi tra loro — è un insight interessante di per sé)
- **Attenzione**: serve un numero minimo di articoli per giornalista (almeno 30-50) per un training sensato — verifica questo vincolo prima di investirci tempo

#### Giorno 6 (se in anticipo) — Distanza lessicale / ipotesi AI adoption

- Concetti: sentence embedding, similarità coseno
- Strumenti: `sentence-transformers` (modello multilingue pre-addestrato, no training necessario — perfetto per Colab)
- Calcola embedding medio per giornalista per anno, misura distanza anno-su-anno
- ⚠️ **Cautela metodologica importante**: un salto nella distanza lessicale è una correlazione debolissima con "adozione AI" — ci sono decine di altre spiegazioni (cambio di sezione, cambio di stile editoriale, evento eccezionale che genera vocabolario nuovo). Nel report, presenta questo come _ipotesi esplorativa da validare_, non come conclusione. Un recruiter che ti vede affermare "questo prova l'uso di AI" senza questa cautela penserà che non capisci i limiti della tua analisi — è un rischio di credibilità, non un vantaggio.

#### Giorno 7 — Power BI + video

- Importa i CSV/risultati già calcolati in Python (Power BI non deve _fare_ l'analisi, solo _presentarla_)
- Costruisci 3-4 pagine: overview, temi nel tempo, tono, partiti/popolarità (lascia le parti ML/stretch nel notebook, non forzarle in Power BI)
- Registra il video (5-8 min): parti dalla domanda di business, mostra 2-3 momenti chiave del processo tecnico, chiudi sulla dashboard
- Scrivi il README finale con executive summary, metodologia, limiti dichiarati (inclusa la cautela sul punto 6 se l'hai fatto)