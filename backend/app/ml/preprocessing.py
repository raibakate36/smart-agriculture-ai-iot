import pandas as pd


def inspect_dataset(file_path: str):
    """
    Load and inspect an agricultural dataset.
    """

    df = pd.read_csv(file_path)

    print("\n--- Dataset Shape ---")
    print(df.shape)

    print("\n--- Columns ---")
    print(df.columns.tolist())

    print("\n--- Missing Values ---")
    print(df.isnull().sum())

    print("\n--- Duplicate Rows ---")
    print(df.duplicated().sum())

    print("\n--- First 5 Rows ---")
    print(df.head())

    return df