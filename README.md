📊 Financial Decision Support System

An end-to-end Financial Analysis & Decision Support Platform built using Python, Streamlit, and SQLite.
The system allows users to upload financial statements, validate data, simulate business decisions, forecast outcomes, analyze risk, and compare multiple financial scenarios interactively.

🚀 Project Overview
This project is designed to bridge financial analysis and data science by providing a realistic, interpretable, and user-driven financial modeling tool.

Key Capabilities
Upload and validate Income Statement and Balance Sheet data
Automatic data cleaning and anomaly detection
Financial ratio analysis
Scenario-based forecasting with realistic assumptions
Break-even analysis
Cash-flow analysis (CFO, CFI, CFF)
Risk sensitivity (tornado analysis)
Scenario persistence and comparison
Executive-level dashboards and insights

🧠 Why This Project Matters

Unlike black-box ML models, this system focuses on:
Interpretability
Financial realism
Decision support
Scenario comparison

It reflects how real financial analysts and decision makers evaluate business strategies.

🛠️ Tech Stack
Component	Technology
Language	Python
UI	Streamlit
Database	SQLite
Visualization	Plotly
Data Handling	Pandas
Storage	Local SQLite DB
Cost	100% Free & Open-Source

✔ Runs on CPU only
✔ Works on Intel i5 + Iris Xe
✔ No paid APIs
✔ No heavy registration

📁 Project Structure
financial_decision_app/
│
├── app.py                     # Main Streamlit dashboard
├── data_loader.py              # CSV ingestion
├── validator.py                # Validation & anomaly handling
├── financial_metrics.py        # Ratios & metrics
├── forecasting.py              # Forecasting & break-even logic
├── cashflow.py                 # Cash-flow calculations
├── insights.py                 # Auto-generated insights
├── storage.py                  # SQLite persistence
│
├── scenarios.db                # Persistent scenario storage
├── test_forecasting.py         # Unit test for forecasting
├── README.md                   # Project documentation
└── requirements.txt



📥 Input Data Requirements
Income Statement CSV
Mandatory columns:
Year
Revenue
Operating_Expense
Net_Income
Balance Sheet CSV

Mandatory columns:
Year
Total_Assets
Total_Liabilities
Equity

✔ Extra columns are ignored
✔ Non-numeric values are handled
✔ Duplicate years are detected

🔍 Data Validation Modes

The user can choose how data issues are handled:

Mode	Behavior
strict	Rejects files with any anomaly
auto_clean	Cleans silently
auto_clean_warn	Cleans + shows warnings (recommended)
📊 Dashboard Features
🔹 KPI Cards
Revenue
Net Income
ROE
Debt Ratio

🔹 Financial Charts
Revenue & Net Income trend
Operating & Net profit margins
Debt ratio over time

🔹 Break-Even Analysis
Break-even revenue calculation
Forecast revenue vs break-even chart

🔹 Cash-Flow Statement (Simplified)
CFO (Operating)
CFI (Investing)
CFF (Financing)

🔮 Forecasting Model (Realistic)
The forecasting engine models:
Revenue growth
Variable costs (% of revenue)
Fixed operating costs
Interest expense on debt
Corporate tax
Debt change over time
Net Income Logic (Simplified)
EBIT = Revenue − (Fixed Cost + Variable Cost)
Interest = Debt × Interest Rate
Tax = max(EBIT − Interest, 0) × Tax Rate
Net Income = (EBIT − Interest) − Tax

⚠️ Risk & Sensitivity Analysis
Tornado-style sensitivity chart
Measures impact of assumption changes on net income
Helps identify high-risk drivers

📂 Scenario Management
Save scenarios with assumptions
Persist data using SQLite
View, compare, and delete scenarios
Compare multiple forecast paths visually
All scenarios persist even after restarting the app.

🧾 Auto-Generated Executive Insights
The system automatically generates insights such as:
Revenue growth strength
Profitability trends
Debt risk assessment
Designed for decision makers, not just analysts.

🧪 Testing
A unit test validates the forecasting logic:
python test_forecasting.py

Ensures:
Forecast length correctness
Revenue growth behavior
Data integrity

▶️ How to Run the App
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Start the dashboard
streamlit run app.py
Open in browser:
🚀 Live App: https://financial-decision-support-system-3fetlycsqv2ylqzdz8jwag.streamlit.app/


📌 Use Cases

Financial Analyst portfolio project
Scenario planning tool
Business decision simulation
Finance + Data Science hybrid project
Interview demonstration project

📄 Disclaimer

This tool is for educational and analytical purposes only.
It does not provide financial or investment advice.

👤 Author
[Nimit Kochar]
Aspiring Financial Analyst / Data Scientist

⭐ Final Note
This project emphasizes:
Financial correctness
Transparency
Decision support
Professional software practices
It is intentionally designed to resemble real-world financial analysis workflows, not just academic exercises.
