"""
Script per unire tutti i CSV della cartella "Full Text CSV" (articoli NYT,
uno o piu' file per anno) in un unico file NYT_news.csv nella cartella del
progetto.

I file sono processati uno alla volta e scritti in append sul file di
destinazione, senza mai tenere tutti i dataset in memoria contemporaneamente:
necessario perche' la cartella contiene ~300 MB di CSV.

Uso:
    python merge_full_text_csv.py
"""

import glob
import os

import pandas as pd

INPUT_DIR = "Full Text CSV"
OUTPUT_PATH = "NYT_news.csv"


def merge_csv_folder(input_dir=INPUT_DIR, output_path=OUTPUT_PATH):
    csv_files = sorted(glob.glob(os.path.join(input_dir, "*.csv")))

    if not csv_files:
        raise FileNotFoundError(f"Nessun CSV trovato in '{input_dir}'")

    if os.path.exists(output_path):
        os.remove(output_path)

    for i, file_path in enumerate(csv_files):
        df = pd.read_csv(file_path)
        # Scrivo l'intestazione solo per il primo file, poi vado sempre in append
        df.to_csv(output_path, mode="a", header=(i == 0), index=False, encoding="utf-8")
        print(f"[{i + 1}/{len(csv_files)}] unito {file_path} ({len(df)} righe)")

    return output_path


if __name__ == "__main__":
    out = merge_csv_folder()
    print(f"File unito salvato in: {out}")
