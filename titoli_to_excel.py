"""
Script riutilizzabile per estrarre solo i titoli delle colonne (l'intestazione)
di un dataset e salvarli in un file Excel.

Pensato per dataset anche molto grandi: NON carica mai l'intero file in
memoria, ma legge solo le righe strettamente necessarie a ricavare i nomi
delle colonne (nrows=0 per il CSV, sola prima riga per l'Excel).

Il file di output viene salvato di default nella STESSA cartella del file di
input, con nome "<nome_input>_col.xlsx" (es. "dataset.csv" -> "dataset_col.xlsx").

Uso da riga di comando:
    python titoli_to_excel.py sample/dataset.csv
    python titoli_to_excel.py sample/dataset.csv -o altra_cartella/titoli.xlsx
    python titoli_to_excel.py input.xlsx --sheet Foglio1 --sep ";"

Uso come modulo:
    from titoli_to_excel import titoli_to_excel
    titoli_to_excel("sample/nyt_metadata_sample.csv")
"""

import argparse
import os

import pandas as pd


def _leggi_intestazione(input_path, sep=",", sheet_name=0, encoding="utf-8"):
    """Legge solo l'intestazione (nomi delle colonne) di un file CSV o Excel,
    senza caricare le righe di dati in memoria.
    """
    ext = os.path.splitext(input_path)[1].lower()

    if ext in (".csv", ".tsv", ".txt"):
        sep = "\t" if ext == ".tsv" else sep
        # nrows=0 fa leggere a pandas solo la riga di intestazione
        header_df = pd.read_csv(input_path, sep=sep, encoding=encoding, nrows=0)
    elif ext in (".xlsx", ".xls", ".xlsm"):
        # nrows=0 funziona anche per Excel: engine legge solo la prima riga
        header_df = pd.read_excel(input_path, sheet_name=sheet_name, nrows=0)
    else:
        raise ValueError(f"Formato file non supportato: {ext}")

    return list(header_df.columns)


def _output_path_default(input_path):
    """Costruisce il percorso di output "<nome_input>_col.xlsx" nella stessa
    cartella del file di input.
    """
    cartella = os.path.dirname(input_path)
    nome_senza_estensione = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(cartella, f"{nome_senza_estensione}_col.xlsx")


def titoli_to_excel(input_path, output_path=None,
                     sep=",", sheet_name=0, encoding="utf-8"):
    """Estrae i titoli delle colonne da input_path e li salva in un file Excel.

    Parametri
    ----------
    input_path : str
        Percorso del dataset di origine (CSV o Excel), anche molto grande.
    output_path : str o None
        Percorso del file Excel di output. Se None (default), viene salvato
        nella stessa cartella di input_path con nome "<nome_input>_col.xlsx".
    sep : str
        Separatore usato nel CSV di origine (ignorato per l'Excel).
    sheet_name : str o int
        Foglio da cui leggere l'intestazione, se input_path e' un Excel.
    encoding : str
        Encoding del CSV di origine (ignorato per l'Excel).

    Ritorna
    -------
    str
        Il percorso del file Excel creato.
    """
    if output_path is None:
        output_path = _output_path_default(input_path)

    colonne = _leggi_intestazione(input_path, sep=sep, sheet_name=sheet_name, encoding=encoding)

    # Un dataframe vuoto con i nomi delle colonne del dataset di origine come
    # intestazione: to_excel scrive solo quella riga di titoli, in orizzontale
    titoli_df = pd.DataFrame(columns=colonne)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    titoli_df.to_excel(output_path, index=False, sheet_name="Titoli")

    return output_path


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Estrae solo i titoli delle colonne di un dataset e li salva in Excel."
    )
    parser.add_argument("input_path", help="Percorso del dataset di origine (CSV o Excel)")
    parser.add_argument("-o", "--output", default=None,
                         help="Percorso del file Excel di output "
                              "(default: stessa cartella dell'input, nome '<nome_input>_col.xlsx')")
    parser.add_argument("--sep", default=",", help="Separatore del CSV (default: ',')")
    parser.add_argument("--sheet", default=0, help="Nome o indice del foglio Excel di origine")
    parser.add_argument("--encoding", default="utf-8", help="Encoding del CSV (default: utf-8)")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    output_path = titoli_to_excel(
        args.input_path,
        output_path=args.output,
        sep=args.sep,
        sheet_name=args.sheet,
        encoding=args.encoding,
    )
    print(f"Titoli delle colonne salvati in: {output_path}")
