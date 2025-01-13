# filename: profit_calculator.py

# description: main area handling CSV parsing and orchestrating FIFO logic for pairs,
# preserving "current position" & "PNL" outputs, while counting trades as "open until position=0."

# Copyright (C) 2025 Theodore Knab
# Special thanks to Michael von den Driesch who provided the FIFO logic
# Also Special thanks to ChatGPT

# This file is just a simple implementation of a python class allowing for FIFO bookkeeping

# This is free software: you can redistribute it and/or modify it
# under the terms of the BSD-2-Clause (https://opensource.org/licenses/bsd-license.html).

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the license for more details.

import csv
import os
from datetime import datetime
from collections import defaultdict
from Trade import Trade
from FifoAccount import FifoAccount
import chardet  # Library to detect encoding

def detect_encoding(file_path):
    """Detect the encoding of a CSV file."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def parse_csv(file_path):
    """Parse the CSV file and return processed data."""
    trades = []
    currency_transactions = defaultdict(list)
    reference_transactions = defaultdict(list)
    transaction_types = set()

    # Detect the file encoding
    encoding = detect_encoding(file_path)
    print(f"Detected file encoding: {encoding}")

    try:
        # Open the file with the correct delimiter
        with open(file_path, 'r', encoding=encoding) as file:
            #csv_reader = csv.DictReader(file, delimiter='\t')  # Specify tab delimiter
            csv_reader = csv.DictReader(file, delimiter=',')  # Specify tab delimiter
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

                    one_trade = Trade(
                        date,
                        crypto_asset,
                        crypto_amount,
                        total_amt,
                        crypto_fee,
                        usd_fee,
                        crypto_balance,
                        txid,
                        refid
                    )
                    trades.append(one_trade)
                    currency_transactions[crypto_asset].append(one_trade)
                    reference_transactions[refid].append(one_trade)
                    transaction_types.add(row['type'].strip())
                except KeyError as e:
                    print(f"KeyError: {e} - Check your CSV headers.")
                except ValueError as e:
                    print(f"ValueError: {e} - Check your data types.")
                except UnicodeDecodeError as e:
                    print(f"UnicodeDecodeError: {e} - Ensure the file encoding is correct.")
                    raise

        return trades, currency_transactions, reference_transactions, transaction_types

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e} - Ensure the file exists at the specified path.")



def format_trade_runtime(start_dt, end_dt):
    """Return a string representing how long the trade was open in days/hours/min/sec."""
    if not start_dt or not end_dt:
        return "N/A"
    diff = end_dt - start_dt
    total_sec = diff.total_seconds()
    days = int(total_sec // 86400)
    remainder = int(total_sec % 86400)
    hours = remainder // 3600
    remainder %= 3600
    minutes = remainder // 60
    seconds = remainder % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

if __name__ == "__main__":
    fifo_account = FifoAccount()

    # Use an absolute path to find the CSV file
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'your_file.csv')
    print(f"Debug: File path is {file_path}")

    try:
        trades_list, currency_transactions, reference_transactions, transaction_types = parse_csv(file_path)

        processed_refids = set()

        # For each refid, if exactly 2 trades => process as a pair. 
        # Otherwise => single or partial logic.
        for t in trades_list:
            if t.refid not in processed_refids:
                group = reference_transactions[t.refid]
                if len(group) == 2:
                    # We have a matched pair: USD + crypto
                    usd_trade = next((x for x in group if x.crypto_asset.upper() == 'USD'), None)
                    crypto_trade = next((x for x in group if x.crypto_asset.upper() != 'USD'), None)
                    if usd_trade and crypto_trade:
                        fifo_account.process_trade_pair(usd_trade, crypto_trade)
                    else:
                        # fallback if something is off
                        for g in group:
                            fifo_account.process_single_trade(g)
                else:
                    # Possibly unmatched or partial lines
                    for g in group:
                        fifo_account.process_single_trade(g)

                processed_refids.add(t.refid)

        # After processing all pairs, print final positions & PnL
        fifo_account.print_positions()
        fifo_account.print_pnl()

        print("\nSummary of transactions for all currencies:")
        for ccy, txs in currency_transactions.items():
            print(f"{ccy}: {len(txs)} transactions")

        print("\nTransaction types found:")
        for ttype in sorted(transaction_types):
            print(f"- {ttype}")

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e} - Ensure the file exists at the specified path.")

