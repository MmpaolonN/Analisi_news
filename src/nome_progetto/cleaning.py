def clean_news(df, previous_columns_name, new_columns_name, column_no_missing, column_no_duplicates):
    """
    Clean a news DataFrame: keep and rename the useful columns, then remove
    rows with missing values and duplicates.

    Parameters:
    df (pd.DataFrame): The DataFrame to be cleaned.
    previous_columns_name (list): Current names of the columns to keep. All other columns are dropped.
    new_columns_name (list): New names for the kept columns, in the same order as previous_columns_name.
    column_no_missing (list): Columns (new names) that should not have missing values.
    column_no_duplicates (list): Columns (new names) that should not have duplicate values.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    dict: A report describing what was removed during the cleaning.
    """
    if len(previous_columns_name) != len(new_columns_name):
        raise ValueError("previous_columns_name and new_columns_name must have the same length")

    report = {
        "initial_rows": len(df),
        "initial_columns": len(df.columns),
        "dropped_columns": [col for col in df.columns if col not in previous_columns_name],
    }

    # keep only the useful columns and rename them
    rename_dict = dict(zip(previous_columns_name, new_columns_name))
    df = df[previous_columns_name].rename(columns=rename_dict)

    # remove rows with missing values
    rows_before = len(df)
    df = df.dropna(subset=column_no_missing)
    report["rows_removed_missing"] = rows_before - len(df)

    # remove duplicate rows
    rows_before = len(df)
    df = df.drop_duplicates(subset=column_no_duplicates)
    report["rows_removed_duplicates"] = rows_before - len(df)

    report["final_rows"] = len(df)
    report["final_columns"] = len(df.columns)

    return df, report
