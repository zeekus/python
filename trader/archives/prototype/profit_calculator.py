#filename: profit_calculator.py 
#description main area. 
#Copyright (C) 2025 Theodore Knab
#Special thanks to Michael von den Driesch who provided the FIFO logic
#Also Special thanks to ChatGPT
#This file is just a simple implementation of a python class allowing for FIFO bookkeeping 
#
# This is free software: you can redistribute it and/or modify it
# under the terms of the BSD-2-Clause (https://opensource.org/licenses/bsd-license.html).
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the license for more details.
# Use case download a export of your crypto transactions from Kraken in cvs format.
# rename the ledger.csv to your_csv_file.csv or update the code to user your file name.
# Tested with a kraken ledger.csv export. 
# requires Trade.py 
# requires FifoAccount.py 
# - This was tested and compared to the FIFO calculatations with Bitcoin.tax
import csv
from datetime import datetime
from collections import defaultdict
from Trade import Trade
from FifoAccount import FifoAccount

def parse_csv(file_path):
    trades = []
    currency_transactions = defaultdict(list)
    reference_transactions = defaultdict(list)
    transaction_types = set()

    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            print(f"Processing row: {row}")
            try:
                date = datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S')
                crypto_asset = row['asset'].strip()
                
                crypto_amount = float(row['amount']) if row['amount'] else 0.0
                total_amt = float(row['amountusd']) if row['amountusd'] else 0.0
                crypto_fee = float(row['fee']) if row['fee'] else 0.0
                usd_fee = float(row['fee']) if row['fee'] else 0.0
                crypto_balance = float(row['balance']) if row['balance'] else 0.0
                txid = row['txid'].strip()
                refid = row['refid'].strip()

                trade = Trade(date, crypto_asset, crypto_amount, total_amt, crypto_fee, usd_fee, crypto_balance, txid, refid)
                trades.append(trade)

                currency_transactions[crypto_asset].append(trade)
                reference_transactions[refid].append(trade)
                transaction_types.add(row['type'])

            except KeyError as e:
                print(f"KeyError: {e} - Check your CSV headers.")
            except ValueError as e:
                print(f"ValueError: {e} - Check your data types.")

    return trades, currency_transactions, reference_transactions, transaction_types

if __name__ == "__main__":
    fifo_account = FifoAccount()
    trades_list, currency_transactions, reference_transactions, transaction_types = parse_csv('your_file.csv')

    # Process trades in pairs
    processed_refids = set()
    for trade in trades_list:
        if trade.refid not in processed_refids:
            related_trades = reference_transactions[trade.refid]
            if len(related_trades) == 2:
                usd_trade = next((t for t in related_trades if t.crypto_asset == 'USD'), None)
                crypto_trade = next((t for t in related_trades if t.crypto_asset != 'USD'), None)
                if usd_trade and crypto_trade:
                    fifo_account.process_trade_pair(usd_trade, crypto_trade)
                    processed_refids.add(trade.refid)
            else:
                fifo_account.process_single_trade(trade)
                processed_refids.add(trade.refid)

    fifo_account.print_positions()
    fifo_account.print_pnl()

    print("\nSummary of transactions for all currencies:")
    for currency, transactions in currency_transactions.items():
        print(f"{currency}: {len(transactions)} transactions")

    print("\nTransaction types found:")
    for t_type in sorted(transaction_types):
        print(f"- {t_type}")
