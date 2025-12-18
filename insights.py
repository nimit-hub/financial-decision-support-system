def generate_insights(df):
    insights = []

    rev_growth = (df["Revenue"].iloc[-1] / df["Revenue"].iloc[0]) - 1
    margin_trend = df["Net_Income"].iloc[-1] - df["Net_Income"].iloc[0]
    debt_ratio = df["Total_Liabilities"].iloc[-1] / df["Total_Assets"].iloc[-1]

    if rev_growth > 0.2:
        insights.append("Revenue shows strong long-term growth.")

    if margin_trend > 0:
        insights.append("Profitability has improved over time.")
    else:
        insights.append("Profitability pressure observed.")

    if debt_ratio > 0.6:
        insights.append("High leverage increases financial risk.")
    else:
        insights.append("Debt levels remain manageable.")

    return insights
