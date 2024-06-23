import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.options import Options
from alpha_vantage.fundamentaldata import FundamentalData

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'your_api_key_here')

def fetch_stock_data(symbol, start_date, end_date):
    """
    Fetch historical stock data from Alpha Vantage.

    :param symbol: str : Stock ticker symbol
    :param start_date: str : Start date in format 'YYYY-MM-DD'
    :param end_date: str : End date in format 'YYYY-MM-DD'
    :return: pd.DataFrame : DataFrame containing stock data
    """
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    data, _ = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
    data = data[start_date:end_date]
    return data

def fetch_option_data(symbol):
    """
    Fetch option data from Alpha Vantage.

    :param symbol: str : Stock ticker symbol
    :return: pd.DataFrame : DataFrame containing option data
    """
    fd = FundamentalData(key=ALPHA_VANTAGE_API_KEY)
    options = fd.get_option_chain(symbol)
    all_options_df = pd.DataFrame(options['calls'])
    return all_options_df

if __name__ == "__main__":
    # Example usage
    symbol = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    stock_data = fetch_stock_data(symbol, start_date, end_date)
    print(stock_data.head())

    option_data = fetch_option_data(symbol)
    print(option_data.head())
