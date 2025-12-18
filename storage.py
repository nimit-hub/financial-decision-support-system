import sqlite3
import json
from datetime import datetime
import pandas as pd

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "scenarios.db")

# -----------------------------
# Database initialization
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scenarios (
            scenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario_name TEXT,
            created_at TEXT,
            revenue_growth REAL,
            opex_ratio REAL,
            debt_change REAL,
            forecast_json TEXT
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Save scenario
# -----------------------------
def save_scenario(
    scenario_name: str,
    revenue_growth: float,
    opex_ratio: float,
    debt_change: float,
    forecast_df: pd.DataFrame
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    forecast_json = forecast_df.to_json(orient="records")

    cursor.execute("""
        INSERT INTO scenarios (
            scenario_name,
            created_at,
            revenue_growth,
            opex_ratio,
            debt_change,
            forecast_json
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        scenario_name,
        datetime.now().isoformat(),
        revenue_growth,
        opex_ratio,
        debt_change,
        forecast_json
    ))

    conn.commit()
    conn.close()


# -----------------------------
# Load scenarios
# -----------------------------
def load_scenarios():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM scenarios", conn)
    conn.close()
    return df


# -----------------------------
# Load single scenario forecast
# -----------------------------
def load_scenario_forecast(scenario_id: int) -> pd.DataFrame:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT forecast_json FROM scenarios
        WHERE scenario_id = ?
    """, (scenario_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return pd.DataFrame()

    return pd.DataFrame(json.loads(row[0]))
def delete_scenario(scenario_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM scenarios WHERE scenario_id = ?",
        (scenario_id,)
    )

    conn.commit()
    conn.close()
