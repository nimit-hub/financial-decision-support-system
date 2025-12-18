from data_loader import load_income_statement, load_balance_sheet
from validator import validate_income_statement, validate_balance_sheet
from financial_metrics import merge_financials, compute_financial_ratios

income = validate_income_statement(
    load_income_statement("sample_income_statement.csv")
)

balance = validate_balance_sheet(
    load_balance_sheet("sample_balance_sheet.csv")
)

merged = merge_financials(income, balance)
metrics = compute_financial_ratios(merged)

print(metrics[[
    "Year",
    "Operating_Margin",
    "Net_Profit_Margin",
    "ROA",
    "ROE",
    "Debt_Ratio"
]])
