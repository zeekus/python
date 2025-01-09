# filename: main.py
# Description: Main area to process trades from CSV file.
# Copyright (C) 2025 Theodore Knab
# Special thanks to Michael von den Driesch who provided the FIFO logic 
# Also Special thanks to ChatGPT

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
            print(f"Processing row: {row}")  # Debugging line to see current row being processed
            try:
                date = datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S')
                crypto_asset = row['asset'].strip()  # Ensure no leading/trailing spaces
                
                # Check for empty strings before converting
                crypto_amount = float(row['amount']) if row['amount'] else 0.0
                usd_amount = float(row['amountusd']) if row['amountusd'] else 0.0 if row['type'] == 'sell' else -float(row['amountusd'])
                crypto_fee = float(row['fee']) if row['fee'] else 0.0
                usd_fee = float(row['fee']) if row['fee'] else 0.0
                crypto_balance = float(row['balance']) if row['balance'] else 0.0
                txid = row['txid'].strip()  # Use 'txid' as per your CSV structure

                # Create a Trade instance and append it to trades list
                trade = Trade(date, crypto_asset, crypto_amount, usd_amount, crypto_fee, usd_fee, crypto_balance, txid)
                trades.append(trade)

                # Add transaction details for reporting purposes
                currency_transactions[crypto_asset].append(trade)
                reference_transactions[row['refid']].append(trade)  # Using 'refid' instead of 'reference_id'
                transaction_types.add(row['type'])

            except KeyError as e:
                print(f"KeyError: {e} - Check your CSV headers.")
            except ValueError as e:
                print(f"ValueError: {e} - Check your data types.")

    return trades, currency_transactions, reference_transactions, transaction_types

if __name__ == "__main__":
    fifo_account = FifoAccount()
    trades_list, currency_transactions, reference_transactions, transaction_types = parse_csv('your_file.csv')

    # Process trades grouped by refid
    processed_refids = set()
    for trade in trades_list:
        if trade.txid not in processed_refids:
            fifo_account.process_trade(trade)
            processed_refids.add(trade.txid)

    # Print final positions, cash balance, and PnL
    fifo_account.print_cash_balance()
    fifo_account.print_positions()
    fifo_account.print_pnl()

    # Print summary of transactions for all currencies
    print("\nSummary of transactions for all currencies:")
    for currency, transactions in currency_transactions.items():
        print(f"{currency}: {len(transactions)} transactions")

    # Print all transaction types found
    print("\nTransaction types found:")
    for t_type in sorted(transaction_types):
        print(f"- {t_type}")

