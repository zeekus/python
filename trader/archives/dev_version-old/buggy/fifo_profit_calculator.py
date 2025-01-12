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

 Use case download an export of your crypto transactions from Kraken in csv format.
 rename the ledger.csv to your_csv_file.csv or update the code to use your file name.
 requires Trade.py 
"""

import pandas as pd
from collections import deque

class Trade:
    def __init__(self, date, crypto_asset, crypto_amount, usd_amount, crypto_fee, usd_fee, crypto_balance, transaction_id):
        self.date = date
        self.crypto_asset = crypto_asset
        self.crypto_amount = crypto_amount
        self.usd_amount = usd_amount
        self.crypto_fee = crypto_fee
        self.usd_fee = usd_fee
        self.is_buy = usd_amount < 0  # Buy if USD amount is negative
        self.actual_crypto_amount = crypto_amount - crypto_fee if self.is_buy else crypto_amount
        self.crypto_balance = self.actual_crypto_amount if self.is_buy else crypto_balance
        self.transaction_id = transaction_id  # New attribute for transaction ID

    def print_trade(self, line_number):
        action = "Buying" if self.is_buy else "Selling"
        price = abs(self.usd_amount / self.crypto_amount)
        print(f'{line_number:<3}. Processing trade for {self.crypto_asset:<5}/USD')
        print(f'   Date: {self.date.strftime("%Y-%m-%d")}')
        print(f'   Time: {self.date.strftime("%H:%M:%S")} EST')
        print(f'   Transaction ID: {self.transaction_id}')
        print(f'   Action: {action:<6}')
        print(f'   {self.crypto_asset:<5}: {abs(self.crypto_amount):<10.8f}')
        print(f'   USD: {abs(self.usd_amount):<10.2f}')
        print(f'   Price: {price:<10.2f} USD per {self.crypto_asset}')
        print(f'   Crypto Fee: {self.crypto_fee:<10.8f} {self.crypto_asset}')
        print(f'   USD Fee: {self.usd_fee:<10.2f} USD')
        print(f'   {self.crypto_asset:<5} Balance: {self.crypto_balance:<10.8f}')
        
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
        self.cost_basis = {}

    def buy(self, trade):
        cost_basis = abs(trade.usd_amount) / trade.actual_crypto_amount
        if trade.crypto_asset not in self.positions:
            self.positions[trade.crypto_asset] = deque()
        
        # Add position and update cash balance and fees
        self.positions[trade.crypto_asset].append((trade.actual_crypto_amount, cost_basis))
        self.cash_balance += trade.usd_amount
        self.fees[trade.crypto_asset] = self.fees.get(trade.crypto_asset, 0) + trade.crypto_fee
        self.total_fees += trade.crypto_fee
        
        # Update cost basis record
        if trade.crypto_asset not in self.cost_basis:
            self.cost_basis[trade.crypto_asset] = []
        
        transaction_info = {
            "date": trade.date.strftime("%Y-%m-%d"),
            "time": trade.date.strftime("%H:%M:%S"),
            "transaction_id": trade.transaction_id,
            "amount": trade.actual_crypto_amount,
            "asset_pair": f"{trade.crypto_asset}/USD"
        }
        
        self.cost_basis[trade.crypto_asset].append(transaction_info)

        print(f"Cash balance after buy: ${self.cash_balance:.2f}")
        print(f"Total {trade.crypto_asset} fees: {self.fees[trade.crypto_asset]:.8f}")
        print(f"Cost basis for this buy: ${cost_basis:.2f} per {trade.crypto_asset}")

    def sell(self, trade):
        sell_quantity = abs(trade.crypto_amount)
        
        if trade.crypto_asset not in self.positions or not self.positions[trade.crypto_asset]:
            print(f"Warning: No available positions for selling {trade.crypto_asset}.")
            return
        
        asset_queue = self.positions[trade.crypto_asset]
        
        # Update cash balance with sale proceeds
        self.cash_balance += abs(trade.usd_amount)
        
        total_profit = 0
        quantity_sold = 0

        while sell_quantity > 0 and asset_queue:
            oldest_trade_quantity, oldest_trade_cost_basis = asset_queue[0]
            
            if oldest_trade_quantity <= sell_quantity:
                sell_quantity -= oldest_trade_quantity
                
                # Calculate profit from this sale portion
                sell_price_per_unit = abs(trade.usd_amount / trade.crypto_amount)
                profit_from_sale = (sell_price_per_unit - oldest_trade_cost_basis) * oldest_trade_quantity
                
                total_profit += profit_from_sale
                quantity_sold += oldest_trade_quantity
                
                # Record transaction details for cost basis report
                transaction_info = {
                    "date": trade.date.strftime("%Y-%m-%d"),
                    "time": trade.date.strftime("%H:%M:%S"),
                    "transaction_id": trade.transaction_id,
                    "amount": oldest_trade_quantity,
                    "asset_pair": f"{trade.crypto_asset}/USD"
                }
                if trade.crypto_asset not in self.cost_basis:
                    self.cost_basis[trade.crypto_asset] = []
                self.cost_basis[trade.crypto_asset].append(transaction_info)

                asset_queue.popleft()  # Remove this entry from positions

            else:
                # Partially sell from the oldest position.
                remaining_quantity_after_sell = oldest_trade_quantity - sell_quantity
                
                sell_price_per_unit = abs(trade.usd_amount / trade.crypto_amount)
                profit_from_sale_partial = (sell_price_per_unit - oldest_trade_cost_basis) * sell_quantity
                
                total_profit += profit_from_sale_partial
                quantity_sold += sell_quantity
                
                # Record transaction details for cost basis report.
                transaction_info = {
                    "date": trade.date.strftime("%Y-%m-%d"),
                    "time": trade.date.strftime("%H:%M:%S"),
                    "transaction_id": trade.transaction_id,
                    "amount": sell_quantity,
                    "asset_pair": f"{trade.crypto_asset}/USD"
                }
                if trade.crypto_asset not in self.cost_basis:
                    self.cost_basis[trade.crypto_asset] = []
                self.cost_basis[trade.crypto_asset].append(transaction_info)

                asset_queue[0] = (remaining_quantity_after_sell, oldest_trade_cost_basis)  # Update remaining quantity.
                sell_quantity = 0  # All sold.

            if sell_quantity > 0:
                print(f"Warning: Attempted to sell more {trade.crypto_asset} than available.")

            gross_profit_for_this_sale = total_profit
            
            # Update profit records.
            if trade.crypto_asset not in self.pnl:
                self.pnl[trade.crypto_asset] = 0
            
            # Update total gross profit.
            self.pnl[trade.crypto_asset] += gross_profit_for_this_sale
            
            average_cost_basis_for_this_sale = (oldest_trade_cost_basis * quantity_sold) / quantity_sold if quantity_sold > 0 else 0
            
            print(f'Gross profit for this sale: ${gross_profit_for_this_sale:.2f}')
            print(f'Average cost basis: ${average_cost_basis_for_this_sale:.2f} USD per {trade.crypto_asset}')
            print(f"Running net profit for {trade.crypto_asset}: ${self.pnl[trade.crypto_asset]:.2f}")

    def process_trade(self, trade):
      self.line_number += 1
      trade.print_trade(self.line_number)

      if trade.is_buy:
          self.buy(trade)
      else:
          self.sell(trade)

    def print_positions(self):
      print("\nCurrent Positions:")
      for asset, queue in sorted(self.positions.items()):
          total_quantity = sum(trade[0] for trade in queue)
          if total_quantity > 0:
              total_cost_basis_value = sum(quantity * cost for quantity, cost in queue)
              avg_cost_basis_value = total_cost_basis_value / total_quantity if total_quantity > 0 else 0

              print(f"{asset}: {total_quantity:.8f}")
              print(f"Average Cost Basis: ${avg_cost_basis_value:.2f} per {asset}")
              print("Detailed Cost Basis:")
              for idx, (quantity, cost) in enumerate(queue, start=1):
                  print(f"Lot {idx}: {quantity:.8f} at ${cost:.2f}")

    def print_cash_balance(self):
      print(f"\nCurrent Cash Balance: ${self.cash_balance:.2f}")

    def print_pnl(self):
      print("\nProfit/Loss per Asset:")
      for asset, profit in sorted(self.pnl.items()):
          fees_for_this_asset = self.fees.get(asset, 0)
          net_profit_for_this_asset = profit - fees_for_this_asset
          print(f"{asset:<5}: Taxable Profit: ${net_profit_for_this_asset:.2f}")

      total_gross_profit_value= sum(self.pnl.values())
      total_fees_value= sum(self.fees.values())
      
      print("----------------------------------------")
      print(f"\nTotal [Taxable] Gross Profits: ${total_gross_profit_value:.2f}")
      print(f"Total Fees: ${total_fees_value:.2f}")
      net_total_profit= total_gross_profit_value - total_fees_value 
      print(f"Total [Taxable] Net Profits: ${net_total_profit:.2f}")
      print("----------------------------------------")

    def print_fees(self):
      print("\nTotal Trading Fees per Asset:")
      for asset, fee in sorted(self.fees.items()):
          print(f"{asset}: $ {fee:.2f}")
      total_fees_value= sum(self.fees.values())
      print(f"Total Fees: ${total_fees_value:.2f}")

    def print_cost_basis(self):
      print("\nDetailed Cost Basis:")
      for asset, transactions in sorted(self.cost_basis.items()):
          for idx, info in enumerate(transactions, start=1):
              print(f"{asset}:")
              print(f"Lot {idx}:")
              print(f"Date: {info['date']}")
              print(f"Time: {info['time']} EST")
              print(f"Transaction ID: {info['transaction_id']}")
              print(f"Amount Sold: {info['amount']:.8f} ({info['asset_pair']})")

# Read the CSV file (update to your actual file path)
df = pd.read_csv('your_csv_file.csv', sep='\t', quotechar='"')

# Initialize the FIFO account
fifo_account = FifoAccount()

# Process trades in pairs (assuming trades are paired correctly)
for i in range(0, len(df), 2):
    if i + 1 < len(df):
        row1 = df.iloc[i]
        row2 = df.iloc[i + 1]

        if row1['type'] == 'trade' and row2['type'] == 'trade':
            date_time_str1= row1['time']
            date_time_str2= row2['time']
            
            date_time_utc_1= pd.to_datetime(date_time_str1)
            date_time_utc_2= pd.to_datetime(date_time_str2)

            # Assuming we want to use the first date as reference.
            date_time_utc= date_time_utc_1

            # Generate a unique transaction ID (you can customize this logic)
            transaction_id= f'Trade-{i//2 + 1}' 

            if row1['asset'] == 'USD':
                usd_row= row1 
                crypto_row= row2 
            else:
                usd_row= row2 
                crypto_row= row1 

            crypto_asset= crypto_row['asset']
            crypto_amount= float(crypto_row['amount'])
            usd_amount= float(usd_row['amount'])
            crypto_fee= float(crypto_row['fee'])
            usd_fee= float(usd_row['fee'])
            crypto_balance= float(crypto_row['balance'])

            # Create a Trade object with all necessary information including transaction ID.
            trade= Trade(date_time_utc ,crypto_asset ,crypto_amount ,usd_amount ,crypto_fee ,usd_fee ,crypto_balance ,transaction_id )
            
            fifo_account.process_trade(trade)

# Print final positions, cash balance, PnL, and detailed cost basis.
fifo_account.print_fees()
fifo_account.print_cash_balance()
fifo_account.print_cost_basis()
fifo_account.print_positions()
fifo_account.print_pnl()

"""
 Copyright (C) 2025 Theodore Knab
 Special thanks to Michael von den Driesch who provided the FIFO logic
 Also Special thanks to ChatGPT

 This file is just a simple implementation of a python class allowing for FIFO bookkeeping

 This *GIST* is free software: you can redistribute it and/or modify it under the terms of the BSD-2-Clause (https://opensource.org/licenses/bsd-license.html).

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the license for more details.

 Use case download an export of your crypto transactions from Kraken in csv format.
 rename the ledger.csv to your_csv_file.csv or update the code to use your file name.
"""

