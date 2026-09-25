# Classificare gli articoli in temi

> Scritto il 2026-09-25 per [[Progetto News]] (Giorno 2 — "distribuzione dei temi nel tempo").
> Basato sui file `extra_cnn.json`, `extra_guardian.json`, `extra_nyt.json` e su un controllo diretto dei CSV puliti.
> Collegato a: [[Guida_configurazione_Python_principianti]]

---

## 0. In breve (le risposte alle tue domande)

| Domanda | Risposta breve |
|---|---|
| **Qual è il metodo migliore per classificare le categorie nei miei temi?** | Parti da una **tabella di mapping** "sezione → tema", compilata a mano in Excel. Ogni sezione riceve un'etichetta: `diretta` (la sezione corrisponde chiaramente a un tema), `ambigua` (dentro c'è di tutto) o `escludi` (pubblicità, cruciverba…). È veloce, trasparente e già risponde in parte alla prima domanda. |
| **Ci sono modi alternativi per rispondere alla prima domanda?** | Sì, cinque. Il più importante è classificare **il testo** degli articoli. Poi: scoprire i temi automaticamente (topic modeling), contare parole chiave, usare un LLM, misurare le parole invece del numero di articoli. Tabella al §7. |
| **E se scelgo più temi di quelli coperti dalle sezioni?** | Sì, **devi classificare tramite il testo**. Non per tutti gli articoli, però: le sezioni `diretta` le tieni e anzi le usi come **esempi per insegnare al modello**. Il modello classifica solo le sezioni `ambigue` e il NYT. |
| **Con cosa?** | Un **modello di embedding** (`sentence-transformers`) che trasforma ogni articolo in numeri, più un **classificatore** (`scikit-learn`, Logistic Regression) addestrato sugli articoli delle sezioni `diretta`. Gira sul tuo PC, è gratis e lo verifichi con 300-500 articoli etichettati a mano. |

> ⚠️ **Nel tuo caso servirà quasi certamente il testo, anche con pochi temi.** I dati lo mostrano (§1): circa **il 48% di CNN, il 34% del Guardian e quasi tutto il NYT** stanno in sezioni che non dicono di cosa parla l'articolo.

---

## 1. Cosa dicono i tuoi dati (prima di scegliere il metodo)

### 1.1 Numeri principali

| Testata | Articoli | Anni | Colonne "tema" disponibili | Cosa c'è dentro davvero |
|---|---|---|---|---|
| **CNN** | 37.949 | 2011-2022 | `Category` (9 valori), `Section` (55) | Category `news` = **18.077 articoli (48%)**, tutti in sezioni **geografiche**: `europe` (10.635!), `us`, `uk`, `world`, `australia`, `asia`. In `europe` trovi incendi in Grecia, Putin, migranti, Sacha Baron Cohen: di tutto. |
| **Guardian** | 148.720 | 2016-2022 (2022 solo fino a giugno) | `sectionName` (159 valori) | Sezioni ricche e utili (Environment, Politics, Technology, Film…). Però `World news`, `Australia news`, `US news`, `UK news`, `News` e `Opinion` ≈ **50.000 articoli (34%)** sono geografiche o di formato. 114 sezioni hanno meno di 100 articoli: sono quasi tutte **contenuti sponsorizzati** ("Dairy Australia: …", "BMW: …"). |
| **NYT** | 62.856 | 1985-2018 (circa 2.000 per anno: è un **campione**) | `section_name` (**solo 5**), `type_of_material` (36) | Business Day 34.887, World 24.547, Technology 2.700, Your Money 504, Job Market 218. Le sezioni sono troppo larghe, quindi per il NYT **il tema può venire solo dal testo**. `type_of_material` è il **formato** (News, Letter, Obituary…), non il tema. |

### 1.2 Tre lezioni da questi numeri

1. **Le "sezioni" mescolano tre cose diverse:**
   - **argomento**: Sport, Environment, Politics → è quello che ti serve;
   - **geografia**: europe, World news, Australia news → dice *dove*, non *di cosa*;
   - **formato**: Opinion, Letter, Obituary → dice *che tipo di testo* è.

   I temi devono misurare **solo l'argomento**. Geografia e formato, se ti interessano, vanno in colonne separate.
2. **Il dataset non è "il giornale", è quello che è stato raccolto.** Il 41% di CNN è sport. Il NYT contiene solo le sezioni economia, esteri e tecnologia. Quindi "la distribuzione dei temi del NYT" **non si può misurare** con questi dati: puoi misurarla solo *dentro* quelle sezioni. Va scritto nei limiti del progetto.
3. **Gli anni in comune a tutte e tre le testate sono solo il 2016-2018.** CNN e Guardian condividono il 2016-2022. I confronti tra testate vanno fatti su queste finestre.

> ⚠️ **I dati sono in inglese.** Nella nota [[Progetto News]] sono indicati strumenti per l'italiano (`it_core_news_sm`, `feel-it`). Per questi dataset servono modelli **inglesi**: tutto quello che consiglio sotto lo è.

---

## 2. Concetti da sapere (senza darli per scontati)

| Concetto | Spiegazione semplice |
|---|---|
| **Tema** | L'argomento principale di un articolo (es. "Ambiente e clima"). |
| **Tassonomia** | La lista completa e ordinata dei temi che usi. |
| **Codebook** | Il "regolamento" dei temi: per ognuno una definizione, esempi e regole per i casi dubbi. Serve a te per etichettare in modo coerente e a chi legge il progetto per capire cosa hai misurato. |
| **Single-label / multi-label** | Single-label: ogni articolo ha **un solo** tema (quello principale). Multi-label: può averne più di uno (es. "politica climatica" = Politica + Ambiente). Per un grafico "% per tema" serve il single-label, perché le percentuali devono sommare a 100. |
| **Classificazione supervisionata** | Dai al computer tanti esempi già etichettati ("questo articolo è Sport") e lui impara a etichettare quelli nuovi. |
| **Non supervisionata (topic modeling)** | Il computer raggruppa da solo gli articoli simili e *ti propone* dei temi. Non scegli tu i temi: li scopri. |
| **Zero-shot** | Il modello classifica senza esempi, solo leggendo il nome o la descrizione del tema. |
| **Embedding** | Una lista di numeri (es. 384) che rappresenta il *significato* di un testo. Testi simili hanno numeri simili. È il modo in cui il computer "capisce" di cosa parla un articolo. |
| **Etichette deboli (weak labels)** | Etichette non fatte a mano ma ricavate in modo automatico e un po' impreciso: nel tuo caso **dalle sezioni**. Un articolo in "Environment" è *quasi sempre* sull'ambiente. Sono tantissime e gratis. |
| **Training set / validation set** | Il training set sono gli esempi da cui il modello impara. Il validation set sono esempi **etichettati a mano e mai visti dal modello**, su cui controlli quanto sbaglia. |
| **Precision, recall, F1** | *Precision*: tra gli articoli che il modello chiama "Sport", quanti lo sono davvero. *Recall*: tra gli articoli davvero di Sport, quanti ne trova. *F1*: la media tra le due. Da 0 a 1, più alto è meglio. |
| **Matrice di confusione** | Una tabella che mostra quali temi il modello confonde tra loro (es. "Economia" scambiata per "Politica"). |
| **Soglia di confidenza** | Il modello dà una probabilità per ogni tema. Se la più alta è bassa (es. < 0,5), l'articolo va in "Incerto" invece di essere forzato in un tema. |

---

## 3. Passo 1 — Creare la lista dei temi

### 3.1 Regole per una buona lista
1. **Mutuamente esclusivi:** due temi non devono sovrapporsi troppo. Se esitano spesso tra "Economia" e "Lavoro", uniscili.
2. **Esaustivi:** ogni articolo deve poter andare da qualche parte. Per questo servono sempre **"Altro"** e **"Incerto"**.
3. **Solo argomenti:** niente geografia (Esteri, Europa) e niente formati (Opinione, Lettere).
4. **Tra 8 e 15 temi.** Con meno di 8 perdi informazione; con più di 15 il modello sbaglia di più e i grafici diventano illeggibili.
5. **Legati alle tue domande.** Il Giorno 4 del progetto riguarda partiti e leader, quindi "Politica" deve esserci e deve essere ben definita.
6. **Stabili nel tempo.** Il tema deve avere senso sia nel 1985 sia nel 2022. "COVID" no, "Salute" sì.

### 3.2 Non partire da zero: usa uno standard
Esistono tassonomie professionali per le notizie. La più usata è **IPTC Media Topics**: lo standard delle agenzie di stampa (Reuters, AP, ANSA), con 17 temi di primo livello. Partire da lì ti fa risparmiare tempo e ti dà un argomento forte nel README ("ho adottato una tassonomia standard del settore").

### 3.3 Una lista di partenza (adattata da IPTC al tuo progetto)

| # | Tema | Cosa include (breve codebook) | Sezioni che lo coprono già |
|---|---|---|---|
| 1 | **Politica** | Elezioni, governi, partiti, parlamenti, leader, politiche pubbliche | Guardian Politics; CNN politics |
| 2 | **Economia e lavoro** | Mercati, aziende, banche, inflazione, occupazione, finanza personale | Guardian Business, Money; NYT Your Money, Job Market |
| 3 | **Guerra, conflitti e terrorismo** | Guerre, attacchi, esercito, diplomazia militare | *nessuna* |
| 4 | **Criminalità e giustizia** | Reati, processi, polizia, tribunali | Guardian Law; CNN justice |
| 5 | **Ambiente e clima** | Clima, inquinamento, energia (aspetto ambientale), natura | Guardian Environment |
| 6 | **Salute** | Malattie, sanità, pandemie, medicina | Guardian Society (in parte); CNN health |
| 7 | **Scienza e tecnologia** | Ricerca, spazio, tech, internet, AI | Guardian Science, Technology; NYT Technology; CNN tech |
| 8 | **Migrazione** | Migranti, rifugiati, confini, asilo | *nessuna* |
| 9 | **Società e istruzione** | Scuola, università, diritti, religione, disuguaglianze | Guardian Education, Society |
| 10 | **Cultura e spettacolo** | Cinema, musica, TV, libri, arte, celebrità | Guardian Film, Music, Books, Stage, Television & radio, Art and design; CNN entertainment |
| 11 | **Sport** | Tutti gli sport | Guardian Sport, Football; CNN sport, football, tennis, golf, motorsport… |
| 12 | **Stile di vita** | Moda, cibo, viaggi, casa, benessere | Guardian Life and style, Fashion, Food, Travel; CNN travel, style |
| 13 | **Disastri e incidenti** | Terremoti, incendi, incidenti, meteo estremo | *nessuna* (CNN weather in parte) |
| — | **Altro** | Articoli validi che non rientrano nei temi sopra | — |
| — | **Incerto** | Articoli su cui il modello non è sicuro | — |

Fai caso ai temi 3, 8 e 13: **nessuna sezione li copre**. È proprio il caso "più temi di quelli delle sezioni" della tua domanda, e vedrai al §5 come gestirlo.

### 3.4 Dimensioni separate (facoltative ma utili)
- **Formato:** notizia, opinione, lettera, necrologio… (da Guardian `Opinion` e NYT `type_of_material`).
- **Area geografica:** dalle sezioni geografiche (CNN `europe`/`us`, Guardian `World news`/`US news`…).

Così non butti via l'informazione delle sezioni geografiche: la usi per un'altra domanda, tipo "di cosa parla la CNN quando scrive dell'Europa?".

---

## 4. Passo 2 — Mappare le sezioni nei temi (metodo base)

### 4.1 Come funziona
Crei un file Excel `mapping_sezioni.xlsx` con una riga per ogni coppia testata-sezione:

| testata | sezione | n_articoli | tema | tipo |
|---|---|---|---|---|
| Guardian | Environment | 4869 | Ambiente e clima | diretta |
| Guardian | Football | 10722 | Sport | diretta |
| Guardian | World news | 15475 | | ambigua |
| Guardian | Opinion | 11963 | | ambigua |
| Guardian | Dairy Australia: Listen to your gut | 3 | | escludi |
| Guardian | Crosswords | … | | escludi |
| CNN | tennis | 2100 | Sport | diretta |
| CNN | europe | 10635 | | ambigua |
| NYT | Technology | 2700 | Scienza e tecnologia | diretta |
| NYT | Business Day | 34887 | | ambigua |

Cosa significa la colonna **tipo**:
- **`diretta`**: la sezione corrisponde chiaramente a un tema. Tieni il tema della sezione.
- **`ambigua`**: la sezione contiene argomenti diversi. Il tema lo deciderà il testo (§5).
- **`escludi`**: non è giornalismo (sponsorizzati, cruciverba, info del giornale, "Help", "About"). Via dal dataset.

**Regola pratica:** metti `diretta` solo se sei sicuro che **almeno 9 articoli su 10** di quella sezione appartengono a quel tema. Nel dubbio, `ambigua`. Per controllare, leggi 20 titoli a caso della sezione.

### 4.2 Codice per creare il file da compilare
```python
# genera la lista di tutte le sezioni con il numero di articoli, da completare in Excel
(df.groupby(["testata", "sezione"]).size().rename("n_articoli").reset_index()
   .sort_values("n_articoli", ascending=False)
   .assign(tema="", tipo="")
   .to_excel("mapping_sezioni.xlsx", index=False))
```
Usa **.xlsx e non .csv**: Excel in italiano salva i CSV con il `;` al posto della `,`, e pandas poi legge una colonna sola. È un classico errore da principiante.

Poi lo applichi:
```python
mappa = pd.read_excel("mapping_sezioni.xlsx")
df = df.merge(mappa[["testata", "sezione", "tema", "tipo"]], on=["testata", "sezione"], how="left")
df = df[df["tipo"] != "escludi"].reset_index(drop=True)
```

### 4.3 Limiti di questo metodo (perché da solo non basta)
- Non assegna nessun tema agli articoli `ambigui` (circa 1/3 di tutto il dataset).
- Non può creare temi che non esistono come sezione (Migrazione, Conflitti, Disastri).
- Le sezioni sono **decisioni editoriali** che cambiano nel tempo (una testata apre una sezione "Climate" nel 2019 e gli articoli sul clima "aumentano" solo sulla carta).
- Ogni testata ha sezioni diverse, quindi il confronto tra testate misura in parte *come organizzano il sito*, non *di cosa scrivono*.

**Valore:** in poche ore hai un primo grafico e, soprattutto, **decine di migliaia di esempi etichettati gratis** per il passo successivo.

---

## 5. Passo 3 — Se i temi sono più delle sezioni: classificare dal testo

### 5.1 Sì, serve il testo. Ma in modo "ibrido"
La strategia consigliata:

```
Articoli ──► sezione "diretta"? ──sì──► tema della sezione  (e diventano ESEMPI per il modello)
               │
               no (ambigua, o NYT)
               ▼
         il modello legge il testo ──► tema previsto + confidenza
                                          │
                                  confidenza < 0,5 ──► "Incerto"
```

### 5.2 Come insegnare al modello i temi che non hanno sezioni
Per Migrazione, Conflitti e Disastri non hai esempi "gratis" dalle sezioni. Li crei così, in circa un'ora per tema:
1. Scrivi una **descrizione in inglese** del tema (es. *"immigration, refugees, asylum seekers, border crossings, deportation"*).
2. Il modello di embedding trova i **300 articoli più simili** a quella descrizione.
3. Li esporti in Excel e **confermi a mano** quelli giusti. Te ne bastano **50-100 buoni**.
4. Li aggiungi agli esempi di training.

```python
query = model.encode(["immigration, refugees, asylum seekers, border crossings, deportation"],
                     normalize_embeddings=True)
df["somiglianza"] = emb @ query[0]          # quanto ogni articolo somiglia alla descrizione
(df.nlargest(300, "somiglianza")[["testata", "titolo", "somiglianza"]]
   .assign(corretto="")                     # scrivi 1 se è davvero Migrazione, 0 se no
   .to_excel("candidati_migrazione.xlsx"))
```

### 5.3 Testo completo o solo l'inizio?
Usa **titolo + primi ~1.500 caratteri** (circa 250 parole). Il motivo è pratico: nel giornalismo l'argomento è quasi sempre chiaro dal titolo e dal primo paragrafo (lo stile "a piramide rovesciata"). In più il modello consigliato legge comunque al massimo ~256 "pezzi di parola" e ignora il resto. Infine, testi corti significano meno RAM e calcoli molto più veloci sul tuo PC.

---

## 6. Quale metodo per classificare il testo? (trade-off)

Il tuo contesto: **~250.000 articoli**, PC con **CPU senza GPU utilizzabile e 7 GB di RAM**, budget zero, progetto da portfolio (quindi deve essere **spiegabile**).

| Metodo | Servono esempi etichettati? | Qualità attesa | Tempo sul tuo PC (250k articoli) | Costo | Spiegabilità | Temi senza sezione? |
|---|---|---|---|---|---|---|
| **Parole chiave** (liste di termini per tema) | No | Bassa-media: perde molti articoli e sbaglia con parole ambigue ("striker" = calciatore o scioperante) | Minuti | 0 | ⭐⭐⭐ Altissima | Sì, se scrivi le liste |
| **Zero-shot NLI** (modello tipo `bart-large-mnli`) | No | Media | ❌ **Giorni** (analizza ogni articolo una volta per ogni tema) | 0 | ⭐ Bassa | Sì |
| **Somiglianza con la descrizione del tema** (embedding, senza training) | No | Media | 1-3 ore (una volta sola) | 0 | ⭐⭐ Media | Sì |
| **TF-IDF + Logistic Regression** | Sì (gratis dalle sezioni) | Media-alta sulla testata su cui impari, peggio sulle altre e sul NYT di 30 anni prima | Minuti | 0 | ⭐⭐⭐ Alta (vedi le parole decisive) | Servono più esempi a mano |
| ✅ **Embedding + Logistic Regression** | Sì (gratis dalle sezioni + 50-100 a mano per i temi nuovi) | **Alta**, e regge meglio i cambi di testata e di decennio | 1-3 ore per gli embedding (una volta sola), poi secondi | 0 | ⭐⭐ Media | **Sì, con pochi esempi** |
| **LLM via API** (Claude, GPT) | No | Alta | Ore | 💰 Significativo su 250k articoli | ⭐⭐ Media (spiega, ma non è sempre ripetibile) | Sì |
| **LLM in locale** (Ollama, già installato) | No | Media-alta | ❌ **Settimane** su CPU | 0 | ⭐⭐ Media | Sì |
| **Fine-tuning di un transformer** (BERT) | Sì | Molto alta | ❌ Giorni su CPU (serve GPU/Colab) | 0 | ⭐ Bassa | Servono più esempi |

### ✅ Scelta consigliata: embedding (`sentence-transformers`) + Logistic Regression (`scikit-learn`)
Perché:
1. **Sfrutta gratis le sezioni** come esempi (decine di migliaia).
2. **Gestisce i temi nuovi** con 50-100 esempi ciascuno.
3. **Gira sul tuo PC** in tempi accettabili: il calcolo pesante si fa una volta e si salva.
4. **Regge i cambi di testata e di epoca** meglio del TF-IDF, perché lavora sul significato e non sulle parole esatte (un articolo del 1985 sull'"Unione Sovietica" e uno del 2022 sulla "Russia" finiscono vicini).
5. **Gli stessi embedding li riusi** per BERTopic (§7) e per il Giorno 6 del progetto (distanza lessicale): un solo calcolo, tre usi.

Il modello consigliato è `all-MiniLM-L6-v2`: inglese, leggero (circa 90 MB) e veloce su CPU.

---

## 7. Modi alternativi per rispondere alla prima domanda ("distribuzione dei temi nel tempo")

| Approccio | Cosa misura | Quando ha senso | Limite principale |
|---|---|---|---|
| **A. Solo mapping delle sezioni** | Come la testata *organizza* i contenuti | Primo grafico veloce (MVP) | Lascia fuori 1/3 degli articoli e tutto il NYT |
| **B. Classificazione del testo (consigliata)** | Di cosa parlano *davvero* gli articoli, con i **tuoi** temi | Analisi principale | Richiede la validazione a mano |
| **C. Topic modeling** (BERTopic) | Temi **scoperti** dai dati, non scelti da te | Per **controllare la tua lista**: se BERTopic trova un grosso gruppo "Brexit" o "COVID" che non sai dove mettere, la lista va rivista | I temi scoperti sono a volte strani e vanno interpretati; poco confrontabili tra testate |
| **D. Conteggio di parole chiave** | Quanto spesso si nomina qualcosa ("climate", "migrant") | Domande specifiche su un argomento preciso | Non è una classificazione completa |
| **E. LLM su un campione** | Come B, ma senza training | Se hai budget e vuoi alta qualità su un campione (es. 5.000 articoli) | Costo; risultati non sempre identici a ogni esecuzione |

**Un'alternativa sulla metrica, non sul metodo:** invece della *% di articoli* per tema puoi misurare la *% di parole* per tema (quanto spazio la testata dedica a un argomento). Un lungo reportage pesa più di una breve. Hai già `word_count` nel NYT e puoi calcolarlo per le altre testate. È un buon grafico in più per il portfolio.

**Consiglio:** B come analisi principale, A come primo passo (serve comunque per B), C come controllo della tua lista su un campione di 30.000 articoli.

```python
from bertopic import BERTopic
campione = df.sample(30_000, random_state=42)
topic_model = BERTopic(min_topic_size=50)
topics, _ = topic_model.fit_transform(campione["testo_breve"].tolist(),
                                      emb[campione.index.to_numpy()])   # riusa gli embedding già calcolati
topic_model.get_topic_info().head(30)       # i 30 temi più grandi con le parole tipiche
```
(Con 7 GB di RAM non fare BERTopic su tutti i 250.000 articoli: usa un campione.)

---

## 8. La pipeline completa, passo per passo

> Ambiente: un progetto `uv` come spiegato in [[Guida_configurazione_Python_principianti]].
> Per torch usa la versione **solo CPU** (sezione 4.5 della guida), poi:
> ```powershell
> uv add pandas pyarrow openpyxl scikit-learn sentence-transformers plotly bertopic
> uv add --dev ipykernel
> ```

### Passo 1 — Un formato unico per le tre testate (e salvataggio in Parquet)
Ogni testata ha colonne con nomi diversi. Le rinomini tutte allo stesso modo, una testata alla volta per non esaurire la RAM:

```python
import pandas as pd

def uniforma(df, testata, data, sezione, titolo, testo, formato=None):
    out = pd.DataFrame({
        "testata": testata,
        "data": pd.to_datetime(df[data], errors="coerce", utc=True),
        "sezione": df[sezione],
        "formato": df[formato] if formato else None,
        "titolo": df[titolo].fillna(""),
        "testo": df[testo].fillna(""),
    })
    out["anno"] = out["data"].dt.year
    out["testo_breve"] = out["titolo"] + ". " + out["testo"].str.slice(0, 1500)
    return out

cnn = pd.read_csv("CNN_articles_cleaned.csv")
cnn = uniforma(cnn, "CNN", "Date published", "Section", "Headline", "Article text")
cnn["titolo"] = cnn["titolo"].str.replace(r" - CNN$", "", regex=True)
cnn.to_parquet("cnn.parquet")
# stessa cosa per Guardian (sectionName, webTitle, bodyContent, webPublicationDate)
# e NYT (section_name, main_headline, body_text, pub_date, formato="type_of_material")
# NYT: pulisci i separatori → df["testo"] = df["testo"].str.replace("**********", " ", regex=False)
```
Poi crei un unico file **leggero**, senza il testo completo, per tutta l'analisi:
```python
cols = ["testata", "data", "anno", "sezione", "formato", "titolo", "testo_breve"]
df = pd.concat([pd.read_parquet(f, columns=cols) for f in ["cnn.parquet", "guardian.parquet", "nyt.parquet"]],
               ignore_index=True)
df.to_parquet("articoli.parquet")
```
(Rileggi il `testo_breve` di CNN: il testo inizia con " (CNN)", che puoi togliere con lo stesso `str.replace`.)

### Passo 2 — Mapping delle sezioni (§4)
Compili `mapping_sezioni.xlsx`, lo applichi e togli gli `escludi`. Salva il risultato. **Da qui in avanti non riordinare né filtrare più `df`**, perché la riga *i* di `df` deve corrispondere alla riga *i* degli embedding.

### Passo 3 — Calcolare gli embedding (una volta sola)
```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
testi = df["testo_breve"].tolist()
blocchi = []
for inizio in range(0, len(testi), 20_000):             # a blocchi: se si interrompe, non perdi tutto
    e = model.encode(testi[inizio:inizio + 20_000], batch_size=64,
                     normalize_embeddings=True, show_progress_bar=True)
    np.save(f"emb_{inizio}.npy", e)
    blocchi.append(e)
emb = np.vstack(blocchi)
np.save("embeddings.npy", emb)                           # ~380 MB; poi basta np.load
```
Stima: **1-3 ore** sul tuo PC. Lancialo e fai altro. Nelle sessioni successive: `emb = np.load("embeddings.npy")`.

### Passo 4 — Creare il set di validazione a mano (PRIMA di addestrare)
È il passo più importante per la credibilità del progetto.
- Estrai **300-500 articoli a caso** dalle sezioni `ambigue` e dal NYT, circa 100-150 per testata.
- Etichettali in Excel seguendo il codebook, **senza guardare le previsioni del modello** (altrimenti ti fai influenzare).
- Non usarli **mai** per il training.

```python
val = df[df["tipo"] != "diretta"].groupby("testata").sample(n=150, random_state=42)
val[["testata", "titolo", "testo_breve"]].assign(tema_manuale="").to_excel("validazione.xlsx")  # l'indice = id della riga
```

### Passo 5 — Preparare gli esempi di training
```python
train = df[df["tipo"] == "diretta"]
train = train.sample(frac=1, random_state=42).groupby("tema").head(3000)   # max 3.000 per tema: lo sport non deve dominare
# + aggiungi gli esempi confermati a mano per Migrazione, Conflitti, Disastri (§5.2)
```

### Passo 6 — Addestrare e valutare
```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X, y = emb[train.index.to_numpy()], train["tema"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

clf = LogisticRegression(max_iter=2000, class_weight="balanced")
clf.fit(X_tr, y_tr)
print(classification_report(y_te, clf.predict(X_te)))        # verifica 1: accordo con le sezioni

val = pd.read_excel("validazione.xlsx", index_col=0)
pred = clf.predict(emb[val.index.to_numpy()])
print(classification_report(val["tema_manuale"], pred))      # verifica 2: la più importante
print(pd.crosstab(val["tema_manuale"], pred))                # matrice di confusione
```
Come leggere i risultati:
- **Verifica 1 molto più alta della verifica 2**: normale. Le sezioni `diretta` sono "facili", gli articoli ambigui no.
- **F1 sotto 0,6 per un tema**: il tema è definito male o si sovrappone a un altro. Guarda la matrice di confusione e valuta se unirlo.
- **Obiettivo indicativo**: F1 medio ≥ 0,75 sulla verifica 2. Riporta il valore nel README, qualunque sia.
- **Controlla il NYT a parte**: se va molto peggio, aggiungi al training 100-200 articoli NYT etichettati a mano.

Quando sei soddisfatto, **riaddestra su tutto il training** (`clf.fit(X, y)`) prima di classificare.

### Passo 7 — Classificare e unire
```python
proba = clf.predict_proba(emb)
df["tema_testo"] = clf.classes_[proba.argmax(axis=1)]
df["confidenza"] = proba.max(axis=1)
df["tema_finale"] = np.where(df["tipo"] == "diretta", df["tema"], df["tema_testo"])
df.loc[(df["tipo"] != "diretta") & (df["confidenza"] < 0.5), "tema_finale"] = "Incerto"
df["metodo"] = np.where(df["tipo"] == "diretta", "sezione", "testo")   # tracciabilità: sai sempre da dove viene il tema
df.drop(columns="testo_breve").to_parquet("articoli_con_temi.parquet")
```
Controlla la quota di "Incerto": se supera il 15-20%, i temi vanno rivisti.

### Passo 8 — Distribuzione dei temi nel tempo
```python
import plotly.express as px

dist = (df.groupby(["testata", "anno"])["tema_finale"]
          .value_counts(normalize=True).rename("quota").reset_index())
fig = px.area(dist, x="anno", y="quota", color="tema_finale", facet_col="testata")
fig.show()
dist.to_csv("distribuzione_temi.csv", index=False)       # per Power BI
```
Sempre **percentuali per testata e per anno**, mai conteggi assoluti: il numero di articoli per anno dipende da come è stato raccolto il dataset, non dal giornale.

---

## 9. Trappole da dichiarare (e che un recruiter apprezza vedere)

1. **Il dataset non rappresenta tutta la testata.** Il NYT contiene solo 5 sezioni (economia, esteri, tecnologia) ed è un campione di ~2.000 articoli l'anno. CNN è per il 41% sport. Scrivilo nei limiti.
2. **Finestre temporali diverse.** Confronti tra tutte e tre le testate solo nel 2016-2018; CNN e Guardian nel 2016-2022. Il 2022 del Guardian si ferma a giugno.
3. **Gli errori del modello spostano le percentuali.** Se il modello confonde spesso "Politica" con "Economia", una delle due risulterà gonfiata. La matrice di confusione te lo dice: citala.
4. **Domain shift.** Il modello impara soprattutto dal Guardian (Regno Unito, 2016-2022) e lo applichi al NYT (USA, 1985-2018): per questo la validazione separata per testata è obbligatoria.
5. **Temi da sezione e temi da testo sono misure un po' diverse.** Tieni la colonna `metodo` e, come controllo, fai il grafico anche solo con gli articoli classificati dal testo.
6. **Single-label semplifica.** Un articolo su "Brexit e economia" finisce in un solo tema. Dichiaralo.

---

## 10. Cassetta degli attrezzi: uno strumento per lavoro

| Lavoro | Strumento | Perché questo |
|---|---|---|
| Gestire l'ambiente Python | **uv** | Vedi [[Guida_configurazione_Python_principianti]] |
| Leggere, pulire, unire i dati | **pandas** | Lo stai già usando |
| Formato dei file di lavoro | **Parquet** | 3-5 volte più piccolo del CSV, molto più veloce, carichi solo le colonne che servono |
| Mapping sezioni ed etichettatura manuale | **Excel** (.xlsx letto con pandas) | Lo conosci e hai già `titoli_to_excel.py` |
| Trasformare il testo in numeri | **sentence-transformers** (`all-MiniLM-L6-v2`) | Veloce su CPU, riusabile per BERTopic e per il Giorno 6 |
| Classificare e valutare | **scikit-learn** (`LogisticRegression`, `classification_report`) | Semplice, veloce e standard; lo userai anche il Giorno 5 |
| Controllare la lista dei temi (scoperta) | **BERTopic** | Riusa gli stessi embedding |
| Grafici nel notebook | **plotly** | Interattivo, già installato |
| Dashboard finale | **Power BI** | Come da piano del Giorno 7 |
| Scrivere ed eseguire il codice | **Jupyter in VS Code** | Il tuo setup attuale |

---

## 11. Checklist

- [ ] Lista dei temi (8-15 + Altro + Incerto) con un codebook di una riga per tema
- [ ] Tre file Parquet uniformati + `articoli.parquet` leggero
- [ ] `mapping_sezioni.xlsx` compilato (diretta / ambigua / escludi)
- [ ] **Primo grafico solo con il mapping** (MVP: la prima domanda ha già una risposta parziale)
- [ ] Embedding calcolati e salvati (`embeddings.npy`)
- [ ] 300-500 articoli di validazione etichettati a mano, **prima** del training
- [ ] 50-100 esempi confermati per ogni tema senza sezione
- [ ] Classificatore addestrato; F1 per tema e matrice di confusione salvati
- [ ] `tema_finale`, `confidenza`, `metodo` per ogni articolo
- [ ] Grafico % temi per anno e testata + CSV per Power BI
- [ ] BERTopic su un campione per controllare la lista
- [ ] Sezione "Limiti" nel README con i punti del §9

**Tempi realistici:** il mapping e il primo grafico richiedono 1 giorno. La pipeline completa con validazione richiede altri 2-3 giorni. Nel piano originale il Giorno 2 conteneva anche la pulizia: conviene dedicare a questa analisi i Giorni 2 e 3 e far slittare il sentiment.
