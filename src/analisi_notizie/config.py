"""Configurazione del progetto: percorsi, parametri del modello di sentiment, topic IPTC e prompt per la validazione con LLM."""

from pathlib import Path

# percorsi
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / ".data"
DATASET_DIR = DATA_DIR / "NYT_sample.csv"  # percorso del file csv, non di una cartella

# modello di sentiment (RoBERTa)
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
CHUNK_SIZE = 510  # il modello accetta al massimo 512 token, meno <s> e </s>
BATCH_SIZE = 16  # chunk elaborati insieme

# topic IPTC Media Topics (nomi mostrati nei grafici)
IPTC_MEDIA_TOPIC = [
    "Politica",
    "Economia e lavoro",
    "Guerra, conflitti e terrorismo",
    "Criminalità e giustizia",
    "Ambiente e clima",
    "Salute",
    "Scienza e tecnologia",
    "Migrazione",
    "Società e istruzione",
    "Cultura e spettacolo",
    "Sport",
    "Stile di vita",
    "Disastri e incidenti",
]

# descrizioni dei topic, nello stesso ordine di IPTC_MEDIA_TOPIC: sono il testo che viene trasformato in embedding.
# In inglese, come gli articoli, così testi e descrizioni stanno nello stesso spazio vettoriale.
IPTC_MEDIA_TOPIC_DESC = [
    "Politics: government, parliament, congress, political parties, elections, voters, laws, ministers, presidents, prime ministers, legislation, political campaigns, diplomacy and foreign policy.",
    "Economy and labour: financial markets, stock exchange, companies, earnings, banks, jobs, unemployment, unions, wages, inflation, GDP, taxes, trade, industry, mergers, personal finance and economic policy.",
    "War, conflict and terrorism: wars, armed conflicts, terrorist attacks, military operations, airstrikes, armed groups, insurgents, bombings, national security, peacekeeping missions and military crises.",
    "Crime and justice: crimes, murders, arrests, trials, verdicts, courts, judges, police investigations, mafia, corruption, fraud, theft, violence, prisons and law enforcement.",
    "Environment and climate: climate change, global warming, pollution, sustainability, renewable energy, biodiversity, wildlife, CO2 emissions, green policies and conservation of natural resources.",
    "Health: medicine, diseases, epidemics, vaccines, hospitals, doctors, healthcare system, medical research, drugs, pandemics, prevention and public health policy.",
    "Science and technology: scientific discovery, research study, experiment, laboratory, physics, chemistry, astronomy, space mission, technological innovation, new technology, invention.",
    "Migration: immigration, migrants, refugees, asylum seekers, border crossings, deportation, integration of immigrants, migration policy and refugee camps.",
    "Society and education: schools, universities, students, teachers, education system, social issues, civil rights, family, inequality, poverty, welfare, religion and social movements.",
    "Culture and entertainment: cinema, films, music, art, books, literature, theatre, celebrities, festivals, exhibitions, television shows and cultural events.",
    "Sport: football, soccer, tennis, basketball, Olympics, athletes, teams, matches, championships, tournaments, sports results and records.",
    "Lifestyle: fashion, beauty, food, recipes, restaurants, travel, tourism, home, relationships, wellness, leisure and practical advice for everyday life.",
    "Disasters and accidents: earthquakes, floods, hurricanes, wildfires, road accidents, plane crashes, building collapses, explosions, natural disasters, emergencies, victims and rescue operations.",
]

SENTIMENT_LABELS = ["negative", "neutral", "positive"]

# validazione con LLM: prompt da incollare nella chat ({topics} e {n} vengono riempiti da llm_prompt_files)
LLM_PROMPT = """Sei un annotatore esperto di notizie. Classifica ciascuno degli articoli qui sotto (New York Times, in inglese).

Per ogni articolo assegna:
1. TOPIC: esattamente UNA delle seguenti etichette, scritta identica (stesse maiuscole, accenti e virgole); il testo dopo i due punti è solo la descrizione:
{topics}
Se un articolo tocca più temi, scegli quello PRINCIPALE.

2. SENTIMENT: esattamente una tra negative, neutral, positive. È il tono complessivo dell'articolo (le notizie riportate e il linguaggio usato):
- negative: eventi o tono prevalentemente negativi (morti, crisi, conflitti, critiche, perdite)
- positive: eventi o tono prevalentemente positivi (successi, progressi, celebrazioni)
- neutral: cronaca fattuale senza un tono chiaro, o positivo e negativo bilanciati

Rispondi SOLO con un CSV, separatore punto e virgola, senza spiegazioni e senza blocchi di codice, con questa intestazione:
id;topic;sentiment
Una riga per articolo, nello stesso ordine, usando l'ID indicato. Devono esserci esattamente {n} righe.

ARTICOLI:
"""

# (nome, colonna dell'LLM, colonna predetta, etichette) per ogni metodo confrontato con l'LLM
LLM_COMPARISONS = [
    ("Topic - embedding", "llm_topic", "pred_topic", IPTC_MEDIA_TOPIC),
    ("Sentiment - VADER", "llm_sentiment", "sentiment_label", SENTIMENT_LABELS),
    ("Sentiment - RoBERTa", "llm_sentiment", "sentiment", SENTIMENT_LABELS),
]
