import re

def normalize_column(col_name: str) -> str:
    """
    Normalize column names by:
    - Lowercasing
    - Removing spaces and special characters
    """
    col = col_name.lower()
    col = re.sub(r"[^a-z0-9]", "", col)
    return col


def map_columns(df_columns, mapping_dict):
    """
    Map user columns to internal standard columns.
    Returns a dictionary: {user_column: standard_column}
    """
    normalized_cols = {col: normalize_column(col) for col in df_columns}
    column_map = {}

    for standard_col, synonyms in mapping_dict.items():
        for user_col, norm_col in normalized_cols.items():
            if norm_col in synonyms:
                column_map[user_col] = standard_col
                break

    return column_map


# ----------------------------
# Column dictionaries
# ----------------------------

INCOME_STATEMENT_MAPPING = {
    "Year": ["year", "fiscalyear", "fy"],
    "Revenue": ["revenue", "sales", "turnover", "netsales"],
    "Operating_Expense": [
    "operatingexpense",
    "operatingcost",
    "operatingcosts",
    "opex",
    "expenses"
    ],

    "Net_Income": ["netincome", "netprofit", "profitaftertax", "pat"]
}

BALANCE_SHEET_MAPPING = {
    "Year": ["year", "fiscalyear", "fy"],
    "Total_Assets": ["totalassets", "assets"],
    "Total_Liabilities": ["totalliabilities", "liabilities"],
    "Equity": ["equity", "shareholdersequity", "networth"]
}
