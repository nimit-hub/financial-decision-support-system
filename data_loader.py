import pandas as pd
from schema_mapper import (
    map_columns,
    INCOME_STATEMENT_MAPPING,
    BALANCE_SHEET_MAPPING
)


def load_income_statement(file):
    df = pd.read_csv(file)

    column_map = map_columns(df.columns, INCOME_STATEMENT_MAPPING)
    df = df.rename(columns=column_map)

    return df


def load_balance_sheet(file):
    df = pd.read_csv(file)

    column_map = map_columns(df.columns, BALANCE_SHEET_MAPPING)
    df = df.rename(columns=column_map)

    return df
