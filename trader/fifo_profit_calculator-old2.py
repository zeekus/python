"""
 Copyright (C) 2025 Theodore Knab
 Special thanks to Michael von den Driesch who provided the FIFO logic
 Also Special thanks to ChatGPT

 This file is just a simple implementation of a python class allowing for FIFO bookkeeping 

 This *GIST* is free software: you can redistribute it and/or modify it
 under the terms of the BSD-2-Clause (https://opensource.org/licenses/bsd-license.html).

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.

 Use case download a export of your crypto transactions from Kraken in cvs format.
 rename the ledger.csv to your_csv_file.csv or update the code to user your file name.
 requires Trade.py 
"""



import pandas as pd
from collections import deque
from Trade import Trade

class FifoAccount:
    def __init__(self):
        self.positions = {}
        self.pnl = {}
        self.cash_balance = 0
        self.line_number = 0
        self.fees = {}
        self.total_fees = 0
        self.total_gross_profit = 0
        self.total_net_profit = 0

    # ... (other methods remain the same)

    def sell(self, trade):
        # ... (existing sell logic)

        gross_profit = total_profit
        net_profit = gross_profit - trade.usd_fee
        self.pnl[trade.crypto_asset] += net_profit
        self.fees[trade.crypto_asset] += trade.usd_fee
        self.total_fees += trade.usd_fee
        self.total_gross_profit += gross_profit
        self.total_net_profit += net_profit

        average_cost_basis = total_cost_basis / quantity_sold if quantity_sold > 0 else 0
        print(f'   Gross profit for this sale: ${gross_profit:9.2f}')
        print(f'   USD fee for this sale: ${trade.usd_fee:.2f}')
        print(f'   Net profit for this sale: ${net_profit:9.2f}')
        print(f'   Average cost basis: ${average_cost_basis:9.2f} USD per {trade.crypto_asset}')
        print(f'   Average sale price: ${abs(trade.usd_amount) / quantity_sold:9.8f} USD per {trade.crypto_asset}')
        print(f"Running net profit for {trade.crypto_asset}: ${self.pnl[trade.crypto_asset]:9.8f}")

    def print_pnl(self):
        print("\nProfit/Loss Breakdown:")
        for asset, profit in self.pnl.items():
            print(f"{asset}:")
            print(f"  Net Profit: ${profit:9.2f}")
            print(f"  Fees: ${self.fees[asset]:9.2f}")
        
        print(f"\nTotal Gross Profit: ${self.total_gross_profit:9.2f}")
        print(f"Total Fees: ${self.total_fees:9.2f}")
        print(f"Total Net Profit: ${self.total_net_profit:9.2f}")

        print("\nDetailed Calculation:")
        print(f"  Total Gross Profit: ${self.total_gross_profit:9.2f}")
        print(f"  Total Fees:         ${self.total_fees:9.2f}")
        print(f"  ----------------------------------------")
        print(f"  Total Net Profit:   ${self.total_net_profit:9.2f}")


    def print_positions(self):
        print("\nCurrent Positions:")
        for asset, queue in self.positions.items():
            total_quantity = sum(trade[0] for trade in queue)
            if total_quantity > 0:
                print(f"{asset}: {total_quantity:6.8f}")

    def print_cash_balance(self):
        print(f"\nCurrent Cash Balance: ${self.cash_balance:9.2f}")

    def print_pnl(self):
        print("\nProfit/Loss per Asset:")
        for asset, profit in self.pnl.items():
            print(f"{asset}: $ {profit:9.2f}")
        print(f"Total PnL: ${sum(self.pnl.values()):9.2f}")

    def print_fees(self):
        print("\nTotal Fees per Asset:")
        for asset, fee in self.fees.items():
            print(f"{asset}: {fee:9.2f}")
        print(f"Total Fees: {sum(self.fees.values()):9.2f}")

# Read the CSV file
df = pd.read_csv('your_csv_file.csv', sep='\t', quotechar='"')

# Initialize the FIFO account
fifo_account = FifoAccount()

# Process trades in pairs
for i in range(0, len(df), 2):
    if i + 1 < len(df):
        row1 = df.iloc[i]
        row2 = df.iloc[i + 1]

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
            fee = float(crypto_row['fee'])
            crypto_balance = float(crypto_row['balance'])

            trade = Trade(date, crypto_asset, crypto_amount, usd_amount, fee, crypto_balance)
            fifo_account.process_trade(trade)

# Print final positions, cash balance, and PnL
fifo_account.print_positions()
fifo_account.print_cash_balance()
fifo_account.print_pnl()

