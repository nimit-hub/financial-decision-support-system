# =====================================================
# IMPORTS
# =====================================================
import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_income_statement, load_balance_sheet
from validator import validate_income_statement, validate_balance_sheet
from financial_metrics import merge_financials, compute_financial_ratios
from forecasting import forecast_financials, calculate_break_even_revenue
from cashflow import compute_cash_flow
from insights import generate_insights
from storage import (
    init_db,
    save_scenario,
    load_scenarios,
    load_scenario_forecast,
    delete_scenario
)

# =====================================================
# PAGE ORDER + SESSION STATE
# =====================================================
PAGES = [
    "Overview",
    "Data Requirements",
    "Upload Data",
    "Dashboard",
    "Decision Inputs",
    "Forecast & Save Scenario",
    "Scenario Management",
    "Scenario Comparison",
    "Risk Sensitivity"
]

if "page" not in st.session_state:
    st.session_state.page = "Overview"

# =====================================================
# PAGE NAVIGATION BUTTONS
# =====================================================
def page_navigation_buttons():
    current_index = PAGES.index(st.session_state.page)

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if current_index > 0:
            if st.button("⬅ Previous"):
                st.session_state.page = PAGES[current_index - 1]
                st.rerun()

    with col3:
        if current_index < len(PAGES) - 1:
            if st.button("Next ➡"):
                st.session_state.page = PAGES[current_index + 1]
                st.rerun()

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Financial Decision Support System",
    layout="wide"
)

st.title("📊 Financial Decision Support System")
st.caption("Financial Analysis • Forecasting • Break-Even • Cash-Flow • Scenarios")

# =====================================================
# INIT DATABASE
# =====================================================
init_db()

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
st.sidebar.header("Navigation")

st.session_state.page = st.sidebar.radio(
    "Go to",
    PAGES,
    index=PAGES.index(st.session_state.page)
)

validation_mode = st.sidebar.selectbox(
    "Data Validation Mode",
    ["auto_clean_warn", "auto_clean", "strict"],
    index=0
)

page = st.session_state.page

# =====================================================
# SESSION VARIABLES
# =====================================================
for key in [
    "income_df", "balance_df", "merged_df", "forecast_df",
    "revenue_growth", "variable_cost_ratio", "fixed_cost",
    "tax_rate", "interest_rate", "debt_change"
]:
    if key not in st.session_state:
        st.session_state[key] = None

# =====================================================
# OVERVIEW
# =====================================================
if page == "Overview":
    st.header("🔍 What Can This App Do?")

    st.markdown("""
This application provides **end-to-end financial decision support**
using structured financial statements.

It enables:
- Financial performance analysis
- Cost & break-even analysis
- Cash-flow evaluation
- Forecasting & scenario planning
- Risk & sensitivity analysis
""")

    st.subheader("🚀 How to Use")
    st.markdown("""
1. Upload Income Statement & Balance Sheet  
2. Review historical performance  
3. Adjust decision inputs  
4. Forecast and save scenarios  
5. Compare strategies and assess risk  
""")

    st.divider()
    page_navigation_buttons()

# =====================================================
# DATA REQUIREMENTS
# =====================================================
elif page == "Data Requirements":
    st.header("📄 Data Requirements")

    st.subheader("Income Statement CSV")
    st.code("""
Year
Revenue
Operating_Expense
Net_Income
""")

    st.subheader("Balance Sheet CSV")
    st.code("""
Year
Total_Assets
Total_Liabilities
Equity
""")

    st.divider()
    page_navigation_buttons()

# =====================================================
# UPLOAD DATA
# =====================================================
elif page == "Upload Data":
    st.header("Upload Financial Statements")

    income_file = st.file_uploader("Income Statement CSV", type=["csv"])
    balance_file = st.file_uploader("Balance Sheet CSV", type=["csv"])

    if income_file and balance_file:
        try:
            income = validate_income_statement(
                load_income_statement(income_file),
                mode=validation_mode
            )
            balance = validate_balance_sheet(
                load_balance_sheet(balance_file),
                mode=validation_mode
            )

            st.session_state.merged_df = merge_financials(income, balance)
            st.success("Data uploaded and validated successfully")

        except Exception as e:
            st.error(str(e))

    st.divider()
    page_navigation_buttons()

# =====================================================
# DASHBOARD
# =====================================================
elif page == "Dashboard":
    st.header("📊 Executive Dashboard")

    if st.session_state.merged_df is None:
        st.warning("Upload data first.")
    else:
        df = compute_financial_ratios(st.session_state.merged_df)
        latest = df.iloc[-1]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Revenue", f"{latest['Revenue']:,.0f}")
        c2.metric("Net Income", f"{latest['Net_Income']:,.0f}")
        c3.metric("ROE", f"{latest['ROE']:.2%}")
        c4.metric("Debt Ratio", f"{latest['Debt_Ratio']:.2%}")

        st.plotly_chart(
            px.line(df, x="Year", y=["Revenue", "Net_Income"],
                    title="Revenue & Net Income Trend"),
            use_container_width=True
        )

        be = calculate_break_even_revenue(
            st.session_state.fixed_cost,
            st.session_state.variable_cost_ratio
        )
        if be:
            st.metric("Break-Even Revenue", f"{be:,.0f}")

    st.divider()
    page_navigation_buttons()

# =====================================================
# DECISION INPUTS
# =====================================================
elif page == "Decision Inputs":
    st.header("Decision Inputs")

    st.session_state.revenue_growth = st.slider(
        "Revenue Growth (%)", -20, 30, 5
    ) / 100

    st.session_state.variable_cost_ratio = st.slider(
        "Variable Cost (% of Revenue)", 10, 80, 30
    ) / 100

    st.session_state.fixed_cost = st.number_input(
        "Fixed Operating Cost", value=200000, step=50000
    )

    st.session_state.tax_rate = st.slider(
        "Tax Rate (%)", 0, 40, 25
    ) / 100

    st.session_state.interest_rate = st.slider(
        "Interest Rate (%)", 0, 15, 6
    ) / 100

    st.session_state.debt_change = st.slider(
        "Debt Change (%)", -50, 50, 0
    ) / 100

    st.divider()
    page_navigation_buttons()

# =====================================================
# FORECAST & SAVE SCENARIO
# =====================================================
elif page == "Forecast & Save Scenario":
    st.header("Forecast & Save Scenario")

    if st.session_state.merged_df is not None:
        forecast = forecast_financials(
            st.session_state.merged_df,
            revenue_growth=st.session_state.revenue_growth,
            variable_cost_ratio=st.session_state.variable_cost_ratio,
            fixed_cost=st.session_state.fixed_cost,
            tax_rate=st.session_state.tax_rate,
            interest_rate=st.session_state.interest_rate,
            debt_change=st.session_state.debt_change
        )

        st.session_state.forecast_df = forecast

        st.plotly_chart(
            px.line(forecast, x="Year", y="Revenue",
                    color="Type",
                    title="Historical vs Forecast Revenue"),
            use_container_width=True
        )

        name = st.text_input("Scenario Name")
        if st.button("Save Scenario"):
            save_scenario(
                name,
                st.session_state.revenue_growth,
                st.session_state.variable_cost_ratio,
                st.session_state.debt_change,
                forecast
            )
            st.success("Scenario saved")

    st.divider()
    page_navigation_buttons()

# =====================================================
# SCENARIO MANAGEMENT
# =====================================================
elif page == "Scenario Management":
    st.header("Scenario Management")

    scenarios = load_scenarios()
    st.dataframe(scenarios)

    if not scenarios.empty:
        sid = st.selectbox("Delete Scenario", scenarios["scenario_id"])
        if st.button("Delete"):
            delete_scenario(sid)
            st.rerun()

    st.divider()
    page_navigation_buttons()

# =====================================================
# SCENARIO COMPARISON
# =====================================================
elif page == "Scenario Comparison":
    st.header("Scenario Comparison")

    scenarios = load_scenarios()
    selected = st.multiselect(
        "Select Scenarios",
        scenarios["scenario_id"]
    )

    frames = []
    for sid in selected:
        f = load_scenario_forecast(sid)
        f["Scenario"] = sid
        frames.append(f[f["Type"] == "Forecast"])

    if frames:
        comp = pd.concat(frames)
        st.plotly_chart(
            px.line(comp, x="Year", y="Revenue", color="Scenario"),
            use_container_width=True
        )

    st.divider()
    page_navigation_buttons()

# =====================================================
# RISK SENSITIVITY
# =====================================================
elif page == "Risk Sensitivity":
    st.header("Risk Sensitivity Analysis")

    if st.session_state.merged_df is not None:
        base = forecast_financials(
            st.session_state.merged_df
        ).iloc[-1]["Net_Income"]

        impacts = []
        for g in [0.0, 0.10]:
            ni = forecast_financials(
                st.session_state.merged_df,
                revenue_growth=g
            ).iloc[-1]["Net_Income"]
            impacts.append({
                "Growth": f"{int(g*100)}%",
                "Impact": ni - base
            })

        df_imp = pd.DataFrame(impacts)
        st.plotly_chart(
            px.bar(df_imp, x="Impact", y="Growth",
                   orientation="h",
                   title="Net Income Sensitivity"),
            use_container_width=True
        )

    st.divider()
    page_navigation_buttons()
