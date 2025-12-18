from storage import init_db, save_scenario, load_scenarios, load_scenario_forecast
from forecasting import forecast_financials
from financial_metrics import merge_financials
from validator import validate_income_statement, validate_balance_sheet
from data_loader import load_income_statement, load_balance_sheet

# Initialize DB
init_db()

# Prepare data
income = validate_income_statement(
    load_income_statement("sample_income_statement.csv")
)
balance = validate_balance_sheet(
    load_balance_sheet("sample_balance_sheet.csv")
)

merged = merge_financials(income, balance)

forecast_df = forecast_financials(
    merged,
    years_ahead=3,
    revenue_growth=0.08,
    opex_ratio=0.42,
    debt_change=0.03
)

# Save scenario
save_scenario(
    scenario_name="Base Case",
    revenue_growth=0.08,
    opex_ratio=0.42,
    debt_change=0.03,
    forecast_df=forecast_df
)

# Load scenarios
scenarios = load_scenarios()
print(scenarios[["scenario_id", "scenario_name", "created_at"]])

# Load forecast back
scenario_id = scenarios.iloc[0]["scenario_id"]
loaded_forecast = load_scenario_forecast(scenario_id)

print("\nLoaded Forecast:")
print(loaded_forecast.tail())
