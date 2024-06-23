import numpy as np
from scipy.stats import norm

def bsm_option_price(S, K, T, r, sigma, option_type='call'):
    """
    Calculate the Black-Scholes-Merton option price.
    
    S : float : Stock price
    K : float : Strike price
    T : float : Time to maturity (in years)
    r : float : Risk-free rate
    sigma : float : Volatility
    option_type : str : 'call' or 'put'
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    return price

def monte_carlo_option_price(S, K, T, r, sigma, option_type='call', num_simulations=10000):
    """
    Calculate option price using Monte Carlo simulation.
    
    S : float : Stock price
    K : float : Strike price
    T : float : Time to maturity (in years)
    r : float : Risk-free rate
    sigma : float : Volatility
    option_type : str : 'call' or 'put'
    num_simulations : int : Number of simulations
    """
    np.random.seed(0)
    dt = T / num_simulations
    price_paths = np.zeros(num_simulations)
    
    for i in range(num_simulations):
        price_path = S
        for _ in range(int(T/dt)):
            price_path *= np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * np.random.normal())
        if option_type == 'call':
            price_paths[i] = max(price_path - K, 0)
        elif option_type == 'put':
            price_paths[i] = max(K - price_path, 0)
    
    option_price = np.exp(-r * T) * np.mean(price_paths)
    return option_price

if __name__ == "__main__":
    # Example parameters
    S = 100  # Stock price
    K = 100  # Strike price
    T = 1.0    # Time to maturity in years
    r = 0.05 # Risk-free rate
    sigma = 0.2 # Volatility

    bsm_price = bsm_option_price(S, K, T, r, sigma, 'call')
    monte_carlo_price = monte_carlo_option_price(S, K, T, r, sigma, 'call')
    
    print(f"BSM Call Option Price: {bsm_price}")
    print(f"Monte Carlo Call Option Price: {monte_carlo_price}")