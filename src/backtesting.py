import pandas as pd
import numpy as np
from option_pricing import bsm_option_price, monte_carlo_option_price

# Function to generate sample market data
def generate_sample_data():
    dates = pd.date_range(start="2022-01-01", periods=100, freq='B')
    data = {
        'Date': dates,
        'Stock Price': np.random.normal(100, 10, len(dates)),
        'Strike Price': 100,
        'Time to Maturity': np.linspace(1, 0, len(dates)),
        'Risk-free Rate': 0.05,
        'Volatility': 0.2,
        'Market Price': np.random.normal(10, 2, len(dates))
    }
    return pd.DataFrame(data)

# Function to backtest a strategy
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

# Function to calculate performance metrics
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
    # Generate sample data
    data = generate_sample_data()

    # Backtest the strategy using the BSM model
    strategy_data = backtest(data, model='bsm')

    # Calculate performance metrics
    metrics = calculate_performance_metrics(strategy_data)
    
    print("Performance Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # Save the results to a CSV file
    strategy_data.to_csv('backtest_results.csv', index=False)