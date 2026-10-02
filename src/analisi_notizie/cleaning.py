"""Pulizia del dataset di notizie."""


def clean_news(df, previous_columns_name, new_columns_name, column_no_missing, column_no_duplicates):
    """
    Pulisce un DataFrame di notizie: tiene e rinomina le colonne utili, poi
    rimuove le righe con valori mancanti e i duplicati.

    Parameters:
    df (pd.DataFrame): Il DataFrame da pulire.
    previous_columns_name (list): Nomi attuali delle colonne da tenere. Tutte le altre vengono eliminate.
    new_columns_name (list): Nuovi nomi delle colonne tenute, nello stesso ordine di previous_columns_name.
    column_no_missing (list): Colonne (nuovi nomi) che non devono avere valori mancanti.
    column_no_duplicates (list): Colonne (nuovi nomi) che non devono avere valori duplicati.

    Returns:
    pd.DataFrame: Il DataFrame pulito.
    dict: Un report di cosa è stato rimosso durante la pulizia.
    """
    if len(previous_columns_name) != len(new_columns_name):
        raise ValueError("previous_columns_name and new_columns_name must have the same length")

    report = {
        "initial_rows": len(df),
        "initial_columns": len(df.columns),
        "dropped_columns": [col for col in df.columns if col not in previous_columns_name],
    }

    # tengo solo le colonne utili e le rinomino
    rename_dict = dict(zip(previous_columns_name, new_columns_name))
    df = df[previous_columns_name].rename(columns=rename_dict)

    # rimuovo le righe con valori mancanti
    rows_before = len(df)
    df = df.dropna(subset=column_no_missing)
    report["rows_removed_missing"] = rows_before - len(df)

    # rimuovo le righe duplicate
    rows_before = len(df)
    df = df.drop_duplicates(subset=column_no_duplicates)
    report["rows_removed_duplicates"] = rows_before - len(df)

    report["final_rows"] = len(df)
    report["final_columns"] = len(df.columns)

    return df, report
