import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from config import ASSETS, START_DATE, REPORT_DATE, EXCEL_FILE


def get_ticker_list():
    return [asset["ticker"] for asset in ASSETS.values()]


def download_data():
    """
    Download adjusted close data from Yahoo Finance
    and truncate the dataset to the assignment report date.
    """
    tickers = get_ticker_list()

    raw = yf.download(
        tickers,
        start=START_DATE,
        end=(pd.Timestamp(REPORT_DATE) + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
        auto_adjust=False,
        progress=False
    )

    data = raw["Adj Close"]

    if isinstance(data, pd.Series):
        data = data.to_frame()

    data = data.sort_index()
    data = data.loc[:REPORT_DATE]

    if data.empty:
        raise ValueError(f"No market data available up to report date {REPORT_DATE}.")

    return data


def calculate_returns(data):
    """
    Calculate DTD, MTD, and YTD returns using the fixed assignment date.
    """
    report_date = pd.Timestamp(REPORT_DATE)

    if report_date not in data.index:
        raise ValueError(f"Report date {REPORT_DATE} is not a trading day in downloaded data.")

    # Keep data only up to report date
    data = data.loc[:report_date]

    # DTD: previous trading day -> report date
    dtd = data.pct_change().iloc[-1]

    # MTD: first trading day of December 2024 -> report date
    current_month_data = data[data.index.to_period("M") == report_date.to_period("M")]
    mtd_start = current_month_data.iloc[0]
    mtd = data.iloc[-1] / mtd_start - 1

    # YTD: first trading day of 2024 -> report date
    current_year_data = data[data.index.year == report_date.year]
    ytd_start = current_year_data.iloc[0]
    ytd = data.iloc[-1] / ytd_start - 1

    return {
        "DTD": dtd,
        "MTD": mtd,
        "YTD": ytd
    }


def build_asset_return_summary(returns):
    summary = {}

    for asset_name, asset_config in ASSETS.items():
        ticker = asset_config["ticker"]
        summary[asset_name] = {
            "DTD": returns["DTD"][ticker],
            "MTD": returns["MTD"][ticker],
            "YTD": returns["YTD"][ticker]
        }

    return summary


def get_all_returns():
    data = download_data()
    returns = calculate_returns(data)
    summary = build_asset_return_summary(returns)
    return summary, data


def generate_graphs(data):
    """
    Generate price charts using data up to the report date only.
    """
    for asset_name, asset_config in ASSETS.items():
        ticker = asset_config["ticker"]
        plot_file = asset_config["plot_file"]

        plt.figure()
        data[ticker].plot()
        plt.title(f"{asset_name} Price Trend 2024")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.close()


def create_excel_report(data):
    """
    Export price data up to the report date.
    """
    data.to_excel(EXCEL_FILE)