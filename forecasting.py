import pandas as pd

# =====================================================
# HELPER FUNCTIONS (ADD HERE)
# =====================================================
def calculate_break_even_revenue(fixed_cost, variable_cost_ratio):
    if fixed_cost is None or variable_cost_ratio is None:
        return None

    if variable_cost_ratio >= 1:
        return None

    return fixed_cost / (1 - variable_cost_ratio)

# =====================================================
# MAIN FORECAST FUNCTION
# =====================================================
def forecast_financials(
    historical_df,
    years_ahead=3,
    revenue_growth=0.05,
    variable_cost_ratio=0.30,
    fixed_cost=200000,
    tax_rate=0.25,
    interest_rate=0.06,
    debt_change=0.0
):
    df = historical_df.copy()
    last = df.iloc[-1]

    revenue = last["Revenue"]
    assets = last["Total_Assets"]
    liabilities = last["Total_Liabilities"]

    forecasts = []
    last_year = int(last["Year"])

    for i in range(1, years_ahead + 1):
        year = last_year + i

        revenue *= (1 + revenue_growth)

        variable_cost = revenue * variable_cost_ratio
        operating_cost = fixed_cost + variable_cost
        ebit = revenue - operating_cost

        liabilities *= (1 + debt_change)
        interest = liabilities * interest_rate

        taxable_income = ebit - interest
        tax = max(taxable_income, 0) * tax_rate

        net_income = taxable_income - tax

        assets += net_income
        equity = assets - liabilities

        forecasts.append({
            "Year": year,
            "Revenue": revenue,
            "Operating_Expense": operating_cost,
            "Net_Income": net_income,
            "EBIT": ebit,
            "Interest_Expense": interest,
            "Tax": tax,
            "Total_Assets": assets,
            "Total_Liabilities": liabilities,
            "Equity": equity,
            "Type": "Forecast"
        })

    hist = df.copy()
    hist["Type"] = "Historical"

    return pd.concat([hist, pd.DataFrame(forecasts)], ignore_index=True)
