import pandas as pd
from collections import deque
from Trade import Trade
from FifoAccount import FifoAccount

# Read the CSV file with the correct delimiter (comma)
df = pd.read_csv('your_csv_file.csv', sep=',', quotechar='"')

# Debugging output to check DataFrame structure
print("DataFrame Columns:", df.columns)  # Check column names
print("DataFrame Head:\n", df.head())    # Check first few rows

# Initialize the FIFO account
fifo_account = FifoAccount()

# Process trades in pairs
for i in range(0, len(df), 2):
    if i + 1 < len(df):
        row1 = df.iloc[i]
        row2 = df.iloc[i + 1]

        # Ensure 'type' exists in both rows before accessing it
        if 'type' in row1 and 'type' in row2:
            # Check for trade or deposit types
            if row1['type'] == 'trade' and row2['type'] == 'trade':
                date = pd.to_datetime(row1['time'])

                if row1['asset'] == 'USD':
                    usd_row = row1
                    crypto_row = row2
                else:
                    usd_row = row2
                    crypto_row = row1

                crypto_asset = crypto_row['asset']
                crypto_amount = float(crypto_row['amount'])
                usd_amount = float(usd_row['amount'])
                crypto_fee = float(crypto_row['fee'])
                usd_fee = float(usd_row['fee'])
                crypto_balance = float(crypto_row['balance'])
                txid = row1['refid']  # Assuming refid is what you want to use as txid

                trade = Trade(date, crypto_asset, crypto_amount, usd_amount, crypto_fee, usd_fee, crypto_balance, txid)
                fifo_account.process_trade(trade)

            elif row1['type'] == 'deposit' or row2['type'] == 'deposit':
                # Handle deposit transaction
                deposit_row = row1 if row1['type'] == 'deposit' else row2
                deposit_amount = float(deposit_row['amount'])

                # This messes up the wallet calculation ignore
                # Update cash balance for deposits
                #fifo_account.cash_balance += deposit_amount
                #print(f"Deposit of ${deposit_amount:.2f} received. New cash balance: ${fifo_account.cash_balance:.2f}")
        else:
            print("Error: 'type' column is missing from one of the rows.")

# Summary of trading fees
fifo_account.print_fees()

# Calculate average cost basis after processing trades
##average_costs = fifo_account.calculate_average_cost_basis()

# Print average cost basis on current positions
##print("\nAverage Cost Basis on Current Positions:")
##print("----------------------------------------")
##for asset, avg_cost in average_costs.items():
##    print(f"{asset}: ${avg_cost:.2f} per {asset}")

# Print final positions, cash balance, and PnL
fifo_account.print_positions()
fifo_account.print_pnl()
fifo_account.print_cash_balance()
