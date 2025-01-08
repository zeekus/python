import sys
import pandas as pd
from datetime import datetime

def process_transactions(file):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(file, sep='\t')

    # Convert 'time' to datetime
    df['time'] = pd.to_datetime(df['time'])

    # Filter for trades only
    trades = df[df['type'] == 'trade']

    # Initialize variables for tracking wallet balance and profits
    wallet_balance = 0.0
    profits = {}
    daily_profits = {}

    # Process each trade
    for _, row in trades.iterrows():
        asset = row['asset']
        amount = row['amount']
        amount_usd = row['amountusd']

        # Update wallet balance based on USD trades
        if asset == 'USD':
            wallet_balance += amount_usd

        # Calculate profit/loss for each asset type
        if amount < 0:  # Asset sold
            if asset not in profits:
                profits[asset] = 0.0
            
            gain_loss = -amount_usd  # Selling an asset results in a gain/loss
            profits[asset] += gain_loss
            
            # Track daily profits
            date_str = row['time'].date().isoformat()
            if date_str not in daily_profits:
                daily_profits[date_str] = {}
            if asset not in daily_profits[date_str]:
                daily_profits[date_str][asset] = 0.0
            
            daily_profits[date_str][asset] += gain_loss

        elif amount > 0:  # Asset purchased
            if asset not in profits:
                profits[asset] = 0.0
            
            cost_basis = amount_usd  # Cost basis when buying an asset
            profits[asset] -= cost_basis
            
    return wallet_balance, profits, daily_profits

def print_results(wallet_balance, profits, daily_profits):
    print(f"Wallet Balance: ${wallet_balance:.2f}")
    
    print("\nProfits by Coin Type:")
    for asset, profit in profits.items():
        print(f"{asset}: ${profit:.2f}")

    print("\nDaily Profits:")
    for date, assets in daily_profits.items():
        print(f"Date: {date}")
        for asset, profit in assets.items():
            print(f"  {asset}: ${profit:.2f}")

if __name__ == "__main__":
    # Read from standard input (cat transactions.tsv | python trade_calculator.py)
    input_file = sys.stdin.read()
    
    # Process the transactions and get results
    wallet_balance, profits, daily_profits = process_transactions(input_file)
    
    # Print the results
    print_results(wallet_balance, profits, daily_profits)

