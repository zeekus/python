import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Create date range for simulation
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")

# Simulate BTC prices with random walk
btc_prices = np.cumsum(np.random.normal(0, 1, len(dates))) + 45000

# Define correlations and volatility for each coin
coins = {
    "ETH":  {"corr": 0.96, "vol": 0.02},
    "ADA":  {"corr": 0.94, "vol": 0.04},
    "LTC":  {"corr": 0.88, "vol": 0.04},
    "XRP":  {"corr": 0.88, "vol": 0.03},
    "XLM":  {"corr": 0.88, "vol": 0.05},
    "ALGO": {"corr": 0.86, "vol": 0.06},
    "SUI":  {"corr": 0.71, "vol": 0.07},
    "XMR":  {"corr": 0.67, "vol": 0.08},
    "NEAR": {"corr": 0.46, "vol": 0.10}
}

# Generate correlated price data
price_data = {"BTC": btc_prices}
for coin, params in coins.items():
    # Create correlated noise
    noise = np.random.normal(0, params["vol"], len(dates))
    # Generate prices based on correlation
    price_data[coin] = btc_prices * (1 + params["corr"] * noise)

# Create DataFrame
df = pd.DataFrame(price_data, index=dates)

# Calculate rolling 30-day correlations with BTC
rolling_corr = df.rolling(window=30).corr()["BTC"].drop("BTC")

# Plot results
plt.figure(figsize=(12, 6))
for coin in coins.keys():
    plt.plot(dates, rolling_corr[coin], label=coin)

plt.title("Simulated 30-Day Rolling Correlations with BTC")
plt.xlabel("Date")
plt.ylabel("Correlation Coefficient")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

