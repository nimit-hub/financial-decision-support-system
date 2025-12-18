from data_loader import load_income_statement
from validator import validate_income_statement

df = validate_income_statement(
    load_income_statement("income_anomalous.csv"),
    mode="auto_clean_warn"
)

print(df)
print("WARNINGS:", df.attrs.get("warnings"))
