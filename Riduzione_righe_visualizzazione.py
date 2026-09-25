# visualizzo il contenuto del dataset
import os
import pandas as pd

#Mostra tutte le colonne e righe del DataFrame senza troncamenti
pd.set_option('display.max_columns', None)   # mostra tutte le colonne
pd.set_option('display.max_rows', None)      # mostra tutte le righe (attenzione con df grandi)
pd.set_option('display.width', None)         # non troncare in base alla larghezza terminale
pd.set_option('display.max_colwidth', None)  # non troncare il contenuto delle celle (testo lungo)

os.makedirs("sample", exist_ok=True)

# Esploro il dataset NYT
df_nyt = pd.read_csv("nyt-metadata.csv", nrows=5)
df_nyt.to_csv(os.path.join("sample", "nyt_metadata_sample.csv"), index=False)

# Esploro il dataset Guardian
df_guardian = pd.read_csv("guardian_articles.csv", nrows=5)
df_guardian.to_csv(os.path.join("sample", "guardian_articles_sample.csv"), index=False)

# Esploro il dataset CNN
df_CNN = pd.read_csv("CNN_Articels_clean.csv", nrows=5)
df_CNN.to_csv(os.path.join("sample", "CNN_articles_sample.csv"), index=False)

# Esploro il dataset NYT Full Text
df_nyt_full = pd.read_csv("Full Text CSV/2000_1.csv", nrows=5)
df_nyt_full.to_csv(os.path.join("sample", "nyt_full_sample.csv"), index=False)