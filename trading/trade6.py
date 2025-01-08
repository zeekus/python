import sys
import pandas as pd
from datetime import datetime
from io import StringIO

def process_transactions(file):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(file, sep='\t')

    # Convert 'time' to datetime
    df['time'] = pd.to_datetime(df['time'])

    # Filter for trades only
    trades = df[df['type'] == 'trade']

    # Initialize variables for tracking wallet balance and profits
    initial_wallet_balance = 0.0
    final_wallet_balance = 0.0
    profits = {}
    daily_profits = {}
    open_trades = []

    # Group trades by refid
    grouped_trades = trades.groupby('refid')

    # Process each group of trades
    for refid, group in grouped_trades:
        print(f"\nProcessing RefID: {refid}")
        print(group)  # Debug: Show the group of trades

        # Check if there are open trades (only sells or no corresponding buys)
        if any(group['amount'] < 0) and not any(group['amount'] > 0):
            print(f"Open trade detected for RefID: {refid}")
            for _, row in group.iterrows():
                if row['amount'] < 0:  # Only consider negative amounts (sells)
                    open_trades.append({
                        'refid': refid,
                        'asset': row['asset'],
                        'amount': -row['amount'],  # Store as positive for clarity
                        'time': row['time']
                    })
            continue  # Skip this group

        group_profit = 0.0

        for _, row in group.iterrows():
            asset = row['asset']
            amount = row['amount']
            amount_usd = row['amountusd']
            fee = row['fee'] if 'fee' in row else 0.0  # Get the fee if it exists

            # Update initial wallet balance from the first USD transaction
            if asset == 'USD' and initial_wallet_balance == 0.0:
                initial_wallet_balance += -amount_usd  # Outflow is negative

            # Update final wallet balance based on USD trades
            if asset == 'USD':
                final_wallet_balance += amount_usd
                print(f"Updated final wallet balance (USD): ${final_wallet_balance:.2f}")

            # Calculate profit/loss for each asset type
            if amount < 0:  # Asset sold
                gain_loss = -amount_usd - fee  # Selling an asset results in a gain/loss minus any fees
                group_profit += gain_loss
                
                if asset not in profits:
                    profits[asset] = 0.0
                
                profits[asset] += gain_loss

                # Track daily profits
                date_str = row['time'].date().isoformat()
                if date_str not in daily_profits:
                    daily_profits[date_str] = {}
                if asset not in daily_profits[date_str]:
                    daily_profits[date_str][asset] = 0.0
                
                daily_profits[date_str][asset] += gain_loss
                
                print(f"Processed sale of {abs(amount)} {asset}: Gain/Loss after fees: ${gain_loss:.2f}")

            elif amount > 0:  # Asset purchased
                cost_basis = amount_usd + fee  # Cost basis when buying an asset includes any fees
                group_profit -= cost_basis
                
                if asset not in profits:
                    profits[asset] = 0.0
                
                profits[asset] -= cost_basis

                print(f"Processed purchase of {amount} {asset}: Cost Basis after fees: ${cost_basis:.2f}")

        print(f"RefID: {refid}, Group Profit/Loss: ${group_profit:.2f}")

    return initial_wallet_balance, final_wallet_balance, profits, daily_profits, open_trades

def print_results(initial_wallet_balance, final_wallet_balance, profits, daily_profits, open_trades):
    total_profit = final_wallet_balance - initial_wallet_balance
    
    print(f"\nInitial Wallet Balance: ${initial_wallet_balance:.2f}")
    print(f"Final Wallet Balance: ${final_wallet_balance:.2f}")
    print(f"Total Profit/Loss: ${total_profit:.2f}\n")
    
    print("Profits by Coin Type:")
    for asset, profit in profits.items():
        print(f"{asset}: ${profit:.2f}")

    print("\nDaily Profits:")
    for date, assets in daily_profits.items():
        print(f"Date: {date}")
        for asset, profit in assets.items():
            print(f"  {asset}: ${profit:.2f}")

    print("\nOpen Trades:")
    for trade in open_trades:
        print(f"RefID: {trade['refid']}, Asset: {trade['asset']}, Amount Held: {trade['amount']}, Time: {trade['time']}")

if __name__ == "__main__":
    # Read from standard input (cat transactions.tsv | python trade_calculator.py)
    input_data = sys.stdin.read()
    
    # Use StringIO to treat the string as a file-like object
    input_file = StringIO(input_data)
    
    # Process the transactions and get results
    initial_wallet_balance, final_wallet_balance, profits, daily_profits, open_trades = process_transactions(input_file)
    
    # Print the results
    print_results(initial_wallet_balance, final_wallet_balance, profits, daily_profits, open_trades)

