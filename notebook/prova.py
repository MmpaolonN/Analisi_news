import pandas as pd
from nome_progetto.config import DATASET_DIR, DATA_DIR

df = pd.read_csv(DATASET_DIR)
campione = df['body_text'].sample(n=40, random_state=42)

campione.to_csv(DATA_DIR/"NYT_text.csv", index=False)

# for idx, articolo in campione.items():
#     df.loc[idx, "ipct"] = input(f"Articolo: {articolo}\nClassificazione IPCT: ")
#     df.loc[idx, "sentiment"] = input(f"Articolo: {articolo}\nsentiment: ")

# df.to_csv(DATA_DIR/"NYT_sample_with_ipct.csv", index=False)