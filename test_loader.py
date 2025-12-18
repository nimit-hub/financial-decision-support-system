import pandas as pd
from data_loader import load_income_statement

df = pd.read_csv("sample_income.csv")
print(df.head())
