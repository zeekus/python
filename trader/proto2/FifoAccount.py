# FifoAccount.py
# Description: Holds and runs FIFO logic for buys/sells
# Copyright (C) 2025 Theodore Knab
# Special thanks to Michael von den Driesch who provided the FIFO logic
# Also Special thanks to ChatGPT

from collections import defaultdict, deque

class FifoAccount:
    def __init__(self):
        self.positions = defaultdict(deque)
        self.pnl = defaultdict(float)
        self.cash_balance = 0.0
        self.total_fees = 0.0
        self.total_gross_profit = 0.0
        self.line_number = 0  # Initialize line_number here

    def buy(self, trade):
        cost_basis = abs(trade.usd_amount) / trade.actual_crypto_amount if trade.actual_crypto_amount != 0 else 0.0
        
        # Check if cash balance will go negative after this buy
        potential_cash_balance = self.cash_balance + trade.usd_amount  
        if potential_cash_balance < 0:
            print(f"WARNING: Insufficient funds to buy {trade.crypto_asset}. Current Cash Balance: ${self.cash_balance:.2f}, Attempted Buy Amount: ${trade.usd_amount:.2f}")
            return
        
        self.positions[trade.crypto_asset].append((trade.actual_crypto_amount, cost_basis))
        
        # Update cash balance and fees only if the transaction is valid
        self.cash_balance += trade.usd_amount  
        self.total_fees += trade.crypto_fee
        
        print(f"DEBUG: Buy {trade.crypto_asset}: Amount: {trade.actual_crypto_amount}, Cost Basis: {cost_basis}, Cash Balance: {self.cash_balance:.2f}")

    def sell(self, trade):
       sell_quantity = abs(trade.crypto_amount)
       asset_queue = self.positions[trade.crypto_asset]
       total_profit = 0.0

       while sell_quantity > 0 and asset_queue:
           oldest_trade = asset_queue[0]
           if oldest_trade[0] <= sell_quantity:
               sell_quantity -= oldest_trade[0]
               buy_price = oldest_trade[1]
               profit = (abs(trade.usd_amount) / trade.crypto_amount - buy_price) * oldest_trade[0]
               total_profit += profit
               asset_queue.popleft()
           else:
               buy_price = oldest_trade[1]
               profit = (abs(trade.usd_amount) / trade.crypto_amount - buy_price) * sell_quantity
               total_profit += profit
               asset_queue[0] = (oldest_trade[0] - sell_quantity, buy_price)
               sell_quantity = 0

       if sell_quantity > 0:
           print(f"Warning: Attempted to sell more {trade.crypto_asset} than available")

       # Update PnL after selling.
       self.pnl[trade.crypto_asset] += total_profit

       print(f"DEBUG: Sell {trade.crypto_asset}: Quantity Sold: {trade.crypto_amount}, Total Profit: {total_profit:.2f}, Cash Balance: {self.cash_balance:.2f}")

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
          if abs(total_quantity) > 1e-10:
              print(f"{asset}: {total_quantity:.8f}")

    def print_cash_balance(self):
        print(f"\nCurrent Cash Balance: ${self.cash_balance:.2f}")

    def print_pnl(self):
      print("\nProfit/Loss per Asset:")
      for asset, profit in sorted(self.pnl.items()):
          print(f"{asset}: ${profit:.2f}")

