import pandas as pd
from datetime import datetime
import fileinput
import sys
import argparse
from collections import defaultdict

def print_help():
    """
    Print detailed help instructions for using the trade calculator.
    """
    help_text = """
Trade Profit Calculator

Usage:
  1. Read from a file:
     python trade_calculator.py -i mytransactions.tsv

  2. Read from standard input:
     cat mytransactions.tsv | python trade_calculator.py

  3. Display help:
     python trade_calculator.py -h or --help

Input File Requirements:
- Tab-separated values (.tsv)
- Must include columns: txid, refid, time, type, asset, amount, fee
- First row should be column headers

Example input file format:
txid    refid    time                      type    subtype    aclass    asset    wallet    amount      fee    balance      amountusd
LFWBMP-6KB4V-XXC6PU    TQBES7-AENPX-HHJ3J5    "2025-01-01 16:33:06"    trade    currency    USD    spot / main    -979.3789   0       0           -979.38

Options:
  -i, --input     Specify input file path
  -h, --help      Show this help message
"""
    print(help_text)

def load_data(input_file=None):
    """
    Load the data from STDIN or a file into a pandas DataFrame.
    """
    data = []
    
    # If input file is specified, use fileinput to read from file or stdin
    if input_file:
        try:
            with open(input_file, 'r') as f:
                data = [line.strip().split('\t') for line in f]
        except FileNotFoundError:
            print(f"Error: File {input_file} not found.")
            sys.exit(1)
    else:
        # Read from stdin if no file specified
        data = [line.strip().split('\t') for line in fileinput.input()]
    
    if len(data) < 2:
        print("Error: Input file is empty or does not contain data.")
        sys.exit(1)

    columns = ['txid', 'refid', 'time', 'type', 'subtype', 'aclass', 'asset', 'wallet', 'amount', 'fee', 'balance', 'amountusd']
    df = pd.DataFrame(data[1:], columns=columns)  # Skip the header row
    
    # Remove quotes from all columns
    for col in df.columns:
        df[col] = df[col].str.replace('"', '')
    
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    
    # Convert numeric columns, replacing empty strings with NaN
    numeric_cols = ['amount', 'fee', 'balance', 'amountusd']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def calculate_profits(df):
    """
    Calculate profits per trade and track total profit per asset.
    """
    profits = []
    open_positions = defaultdict(list)
    asset_profits = defaultdict(float)
    total_profit = 0
    usd_balance = 0

    for _, row in df.iterrows():
        if row['type'] == 'trade':
            asset = row['asset']
            amount = row['amount']
            fee = row['fee']

            if asset == 'USD':
                # Update USD balance directly without calculating profit.
                usd_balance += amount - fee
                continue

            if amount > 0:  # Buying asset
                # Record the purchase with its cost.
                open_positions[asset].append({'amount': amount, 'cost': abs(row['amountusd'])})
            else:  # Selling asset
                sell_amount = abs(amount)
                sell_value = abs(row['amountusd'])

                while sell_amount > 0 and open_positions[asset]:
                    buy = open_positions[asset][0]  # Get the oldest buy order
                    
                    if buy['amount'] <= sell_amount:
                        # If selling more than or equal to what was bought
                        profit = (sell_value * (buy['amount'] / abs(amount))) - buy['cost'] - fee
                        sell_amount -= buy['amount']
                        open_positions[asset].pop(0)  # Remove the position if fully sold
                    else:
                        # If selling less than what was bought
                        profit = (sell_value * (sell_amount / abs(amount))) - (buy['cost'] * (sell_amount / buy['amount'])) - fee
                        buy['amount'] -= sell_amount  # Reduce the amount of the open position
                        sell_amount = 0  # All sell amount has been accounted for
                    
                    profits.append({
                        'time': row['time'],
                        'refid': row['refid'],
                        'asset': asset,
                        'profit': profit
                    })
                    asset_profits[asset] += profit
                    total_profit += profit

    return pd.DataFrame(profits), asset_profits, total_profit, usd_balance


def main():
    """
    Main function to process the data and calculate profits.
    """

    # Set up argument parser.
    parser = argparse.ArgumentParser(description='Trade Profit Calculator')
    parser.add_argument('-i', '--input', help='Input TSV file path')
    
    # The -h/--help option is automatically added by argparse, so we don't need to define it.

    # Parse arguments.
    args = parser.parse_args()

    # Show help if requested (this will be handled automatically by argparse).
    if args.input is None:
        print_help()
        sys.exit(0)

    # Load data from file or stdin.
    df = load_data(args.input)

    # Calculate profits and retrieve USD balance.
    profits_df, asset_profits, total_profit, usd_balance = calculate_profits(df)

    # Output results.
    print("Profits per trade:")
    print(profits_df)

    print("\nProfits per asset type:")
    for asset, profit in asset_profits.items():
        if asset != "USD":  # Exclude USD from output.
            print(f"{asset}: ${profit:.2f}")

    print(f"\nTotal profit across all assets: ${total_profit:.2f}")
    print(f"\nCurrent USD wallet balance: ${usd_balance:.2f}")

if __name__ == "__main__":
    main()


