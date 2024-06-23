import pandas as pd
import numpy as np
from option_pricing import bsm_option_price, monte_carlo_option_price
from fetch_data import fetch_stock_data, fetch_option_data

def backtest(data, model='bsm'):
    signals = []
    returns = []

    for index, row in data.iterrows():
        S = row['Stock Price']
        K = row['Strike Price']
        T = row['Time to Maturity']
        r = row['Risk-free Rate']
        sigma = row['Volatility']
        market_price = row['Market Price']

        if model == 'bsm':
            model_price = bsm_option_price(S, K, T, r, sigma, 'call')
        elif model == 'monte_carlo':
            model_price = monte_carlo_option_price(S, K, T, r, sigma, 'call')
        else:
            raise ValueError("Model must be 'bsm' or 'monte_carlo'")

        if model_price > market_price:
            signals.append('Buy')
            returns.append(model_price - market_price)
        else:
            signals.append('Sell')
            returns.append(market_price - model_price)

    data['Signals'] = signals
    data['Returns'] = returns
    return data

def calculate_performance_metrics(data):
    total_return = data['Returns'].sum()
    annual_return = np.mean(data['Returns']) * 252
    downside_risk = np.std(data.loc[data['Returns'] < 0, 'Returns'])
    sortino_ratio = annual_return / downside_risk if downside_risk != 0 else np.nan

    metrics = {
        'Total Return': total_return,
        'Annual Return': annual_return,
        'Sortino Ratio': sortino_ratio
    }
    return metrics

if __name__ == "__main__":
    symbol = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    stock_data = fetch_stock_data(symbol, start_date, end_date)
    print(stock_data.head())

    option_data = fetch_option_data(symbol)
    print(option_data.head())

    # Prepare the option data for backtesting
    option_data = option_data.rename(columns={'strike': 'Strike Price', 'lastPrice': 'Market Price'})

    # Merge stock data with option data
    merged_data = stock_data.merge(option_data, left_index=True, right_index=True)

    # Backtest the strategy using the BSM model
    strategy_data = backtest(merged_data, model='bsm')

    # Calculate performance metrics
    metrics = calculate_performance_metrics(strategy_data)
    
    print("Performance Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # Save the results to a CSV file
    strategy_data.to_csv('backtest_results_real_data.csv', index=False)
