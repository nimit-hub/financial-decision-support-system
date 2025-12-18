import pandas as pd
from forecasting import forecast_financials

def test_forecast_basic():
    data = {
        "Year": [2021, 2022, 2023],
        "Revenue": [1000000, 1100000, 1200000],
        "Operating_Expense": [600000, 650000, 700000],
        "Net_Income": [200000, 220000, 250000],
        "Total_Assets": [1500000, 1600000, 1700000],
        "Total_Liabilities": [700000, 750000, 800000],
        "Equity": [800000, 850000, 900000],
    }

    df = pd.DataFrame(data)

    forecast = forecast_financials(
        df,
        years_ahead=2,
        revenue_growth=0.10,
        variable_cost_ratio=0.30,
        fixed_cost=200000,
        tax_rate=0.25,
        interest_rate=0.05,
        debt_change=0.0
    )

    # Assertions
    assert len(forecast) == 5
    assert forecast.iloc[-1]["Revenue"] > df.iloc[-1]["Revenue"]
    assert "Net_Income" in forecast.columns
    assert (forecast["Revenue"] >= 0).all()

    print("Forecast test PASSED")

if __name__ == "__main__":
    test_forecast_basic()
