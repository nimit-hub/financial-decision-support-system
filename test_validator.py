import pandas as pd
from data_loader import load_income_statement
from validator import validate_income_statement

df = load_income_statement("sample_income.csv")
clean_df = validate_income_statement(df)

print(clean_df)
