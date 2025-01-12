"""
#filename: filo_profit_calculator.py 
#description main area. 
 Copyright (C) 2025 Theodore Knab
 Special thanks to Michael von den Driesch who provided the FIFO logic
 Also Special thanks to ChatGPT

 This file is just a simple implementation of a python class allowing for FIFO bookkeeping 

 This is free software: you can redistribute it and/or modify it
 under the terms of the BSD-2-Clause (https://opensource.org/licenses/bsd-license.html).

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.

 Use case download a export of your crypto transactions from Kraken in cvs format.
 rename the ledger.csv to your_csv_file.csv or update the code to user your file name.
 requires Trade.py 
 requires FifoAccount
"""


import pandas as pd
from collections import deque
from Trade import Trade
from FifoAccount import FifoAccount




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
            crypto_fee = float(crypto_row['fee'])
            usd_fee = float(usd_row['fee'])
            crypto_balance = float(crypto_row['balance'])
            txid = row1['refid']  # Assuming refid is what you want to use as txid

            trade = Trade(date, crypto_asset, crypto_amount, usd_amount, crypto_fee, usd_fee, crypto_balance, txid)
            fifo_account.process_trade(trade)

# Print final positions, cash balance, and PnL
fifo_account.print_fees()
fifo_account.print_cash_balance()
fifo_account.print_positions()
fifo_account.print_pnl()


