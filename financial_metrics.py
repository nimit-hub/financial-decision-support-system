import pandas as pd


def merge_financials(
    income_df: pd.DataFrame,
    balance_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge income statement and balance sheet on Year.
    """
    merged = pd.merge(
        income_df,
        balance_df,
        on="Year",
        how="inner"
    )
    return merged


def compute_financial_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute key financial ratios.
    Assumes merged, validated data.
    """
    df = df.copy()

    # -----------------------------
    # Profitability Ratios
    # -----------------------------
    df["Operating_Margin"] = (
        (df["Revenue"] - df["Operating_Expense"]) / df["Revenue"]
    )

    df["Net_Profit_Margin"] = (
        df["Net_Income"] / df["Revenue"]
    )

    # -----------------------------
    # Return Ratios
    # -----------------------------
    df["ROA"] = (
        df["Net_Income"] / df["Total_Assets"]
    )

    df["ROE"] = (
        df["Net_Income"] / df["Equity"]
    )

    # -----------------------------
    # Leverage Ratios
    # -----------------------------
    df["Debt_Ratio"] = (
        df["Total_Liabilities"] / df["Total_Assets"]
    )

    return df
