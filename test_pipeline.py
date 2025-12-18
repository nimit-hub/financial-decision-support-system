from data_loader import load_income_statement, load_balance_sheet
from validator import validate_income_statement, validate_balance_sheet

# Load data
income_df = load_income_statement("sample_income_statement.csv")
balance_df = load_balance_sheet("sample_balance_sheet.csv")

# Validate data
income_clean = validate_income_statement(income_df)
balance_clean = validate_balance_sheet(balance_df)

print("INCOME STATEMENT (CLEAN)")
print(income_clean)

print("\nBALANCE SHEET (CLEAN)")
print(balance_clean)
