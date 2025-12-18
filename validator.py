import pandas as pd

# =====================================================
# Mandatory columns
# =====================================================
INCOME_MANDATORY_COLS = [
    "Year",
    "Revenue",
    "Operating_Expense",
    "Net_Income"
]

BALANCE_MANDATORY_COLS = [
    "Year",
    "Total_Assets",
    "Total_Liabilities",
    "Equity"
]

# =====================================================
# Internal helpers
# =====================================================
def _check_mandatory_columns(df, required_cols, statement_name):
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(
            f"{statement_name} missing mandatory columns: {missing}"
        )


def _convert_numeric(df, cols):
    for col in cols:
        if col != "Year":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _collect_anomalies(df, mandatory_cols):
    anomalies = []

    # Missing mandatory values
    missing_rows = df[df[mandatory_cols].isnull().any(axis=1)]
    if not missing_rows.empty:
        anomalies.append(
            f"{len(missing_rows)} rows have missing mandatory values"
        )

    # Duplicate years
    dup_years = df[df.duplicated(subset="Year")]
    if not dup_years.empty:
        anomalies.append(
            f"Duplicate years detected: {dup_years['Year'].tolist()}"
        )

    # Non-numeric values
    for col in mandatory_cols:
        if col != "Year":
            non_numeric = df[pd.to_numeric(df[col], errors="coerce").isna()]
            if not non_numeric.empty:
                anomalies.append(
                    f"Non-numeric values detected in column: {col}"
                )

    return anomalies

# =====================================================
# Income Statement Validation
# =====================================================
def validate_income_statement(
    df: pd.DataFrame,
    mode: str = "auto_clean_warn"
) -> pd.DataFrame:
    """
    mode:
    - strict            : reject on any anomaly
    - auto_clean        : clean silently
    - auto_clean_warn   : clean and attach warnings (recommended)
    """

    df = df.copy()

    _check_mandatory_columns(df, INCOME_MANDATORY_COLS, "Income Statement")

    anomalies = _collect_anomalies(df, INCOME_MANDATORY_COLS)

    if anomalies and mode == "strict":
        raise ValueError(" | ".join(anomalies))

    # Convert numeric columns
    df = _convert_numeric(df, INCOME_MANDATORY_COLS)

    # Drop rows with missing mandatory values
    df = df.dropna(subset=INCOME_MANDATORY_COLS)

    # Remove duplicate years
    df = df.drop_duplicates(subset="Year")

    # Sort by year
    df = df.sort_values("Year")

    if anomalies and mode == "auto_clean_warn":
        df.attrs["warnings"] = anomalies

    return df

# =====================================================
# Balance Sheet Validation
# =====================================================
def validate_balance_sheet(
    df: pd.DataFrame,
    mode: str = "auto_clean_warn"
) -> pd.DataFrame:
    """
    mode:
    - strict            : reject on any anomaly
    - auto_clean        : clean silently
    - auto_clean_warn   : clean and attach warnings (recommended)
    """

    df = df.copy()

    _check_mandatory_columns(df, BALANCE_MANDATORY_COLS, "Balance Sheet")

    anomalies = _collect_anomalies(df, BALANCE_MANDATORY_COLS)

    if anomalies and mode == "strict":
        raise ValueError(" | ".join(anomalies))

    # Convert numeric columns
    df = _convert_numeric(df, BALANCE_MANDATORY_COLS)

    # Drop rows with missing mandatory values
    df = df.dropna(subset=BALANCE_MANDATORY_COLS)

    # Remove duplicate years
    df = df.drop_duplicates(subset="Year")

    # Sort by year
    df = df.sort_values("Year")

    if anomalies and mode == "auto_clean_warn":
        df.attrs["warnings"] = anomalies

    return df
