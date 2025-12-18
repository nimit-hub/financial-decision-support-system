import pandas as pd

def compute_cash_flow(df):
    """
    Simplified Cash Flow Statement
    CFO ≈ Net Income
    CFI ≈ Change in Assets
    CFF ≈ Change in Liabilities
    """

    df = df.copy()

    df["CFO"] = df["Net_Income"]
    df["CFI"] = -df["Total_Assets"].diff()
    df["CFF"] = df["Total_Liabilities"].diff()

    df[["CFO", "CFI", "CFF"]] = df[["CFO", "CFI", "CFF"]].fillna(0)

    return df
