from pathlib import Path

# path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / ".data"
DATASET_DIR = DATA_DIR / "NYT_sample.csv"  # path of the csv file, not a folder

# sentiment model
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
CHUNK_SIZE = 510  # model max is 512 tokens, minus <s> and </s>
BATCH_SIZE = 16   # chunks processed together

# data
IPCT_MEDIA_TOPIC = [
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
    "Disastri e incidenti"
]

IPCT_MEDIA_TOPIC_DESC = [
    "Politics: government, parliament, congress, political parties, elections, voters, laws, ministers, presidents, prime ministers, legislation, political campaigns, diplomacy and foreign policy.",

    "Economy and labour: financial markets, stock exchange, companies, earnings, banks, jobs, unemployment, unions, wages, inflation, GDP, taxes, trade, industry, mergers, personal finance and economic policy.",

    "War, conflict and terrorism: wars, armed conflicts, terrorist attacks, military operations, airstrikes, armed groups, insurgents, bombings, national security, peacekeeping missions and military crises.",

    "Crime and justice: crimes, murders, arrests, trials, verdicts, courts, judges, police investigations, mafia, corruption, fraud, theft, violence, prisons and law enforcement.",

    "Environment and climate: climate change, global warming, pollution, sustainability, renewable energy, biodiversity, wildlife, CO2 emissions, green policies and conservation of natural resources.",

    "Health: medicine, diseases, epidemics, vaccines, hospitals, doctors, healthcare system, medical research, drugs, pandemics, prevention and public health policy.",

    "Science and technology: scientific discoveries, research, space exploration, technology companies, internet, software, computers, artificial intelligence, robotics, smartphones and telecommunications.",

    "Migration: immigration, migrants, refugees, asylum seekers, border crossings, deportation, integration of immigrants, migration policy and refugee camps.",

    "Society and education: schools, universities, students, teachers, education system, social issues, civil rights, family, inequality, poverty, welfare, religion and social movements.",

    "Culture and entertainment: cinema, films, music, art, books, literature, theatre, celebrities, festivals, exhibitions, television shows and cultural events.",

    "Sport: football, soccer, tennis, basketball, Olympics, athletes, teams, matches, championships, tournaments, sports results and records.",

    "Lifestyle: fashion, beauty, food, recipes, restaurants, travel, tourism, home, relationships, wellness, leisure and practical advice for everyday life.",

    "Disasters and accidents: earthquakes, floods, hurricanes, wildfires, road accidents, plane crashes, building collapses, explosions, natural disasters, emergencies, victims and rescue operations."
]
