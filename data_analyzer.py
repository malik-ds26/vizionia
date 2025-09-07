import pandas as pd

def load_csv(file_path):
    return pd.read_csv(file_path)

def get_column_info(df):
    return {
        col: str(dtype)
        for col, dtype in df.dtypes.items()
    }

def get_summary(df):
    return df.describe(include='all').to_html(classes="dataframe styled-table", border=0)

