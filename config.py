import os

# ===== Asset Configuration =====
# key: internal asset name used in reports
# ticker: Yahoo Finance ticker
# plot_file: output chart file name

ASSETS = {
    "SPX": {
        "ticker": "^GSPC",
        "plot_file": "SPX.jpg"
    },
    "VIX": {
        "ticker": "^VIX",
        "plot_file": "VIX.jpg"
    },
    "AAPL": {
        "ticker": "AAPL",
        "plot_file": "AAPL.jpg"
    }
}

START_DATE = "2024-01-01"
REPORT_DATE = "2024-12-27"
EXCEL_FILE = "market_data.xlsx"

# ===== Email Settings =====
# Set these in a .env file or as environment variables (see .env.example)

SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "")
RECIPIENTS = [r for r in os.environ.get("RECIPIENTS", "").split(",") if r]
EMAIL_SUBJECT = "Market Report"