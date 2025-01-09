# filename: FifoAccount.py
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
        self.line_number = 0
        self.wallets = defaultdict(float)

    def process_trade_pair(self, usd_trade, crypto_trade):
      self.line_number += 1
      cost_basis = abs(usd_trade.total_amt / crypto_trade.crypto_amount)
      usd_fee_equivalent = abs(crypto_trade.crypto_fee * cost_basis)
    
      print(f"----------------------------------------")
      print(f"{self.line_number:<3}")
      print(f"...Processing trade pair for {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} linked by {usd_trade.refid}")
      print(f"   Date: {usd_trade.date}")
      print(f"   Action: Pairing transaction")
      print(f"   {usd_trade.crypto_asset:<5}: {abs(usd_trade.crypto_amount):<10.8f}")
      print(f"   {crypto_trade.crypto_asset:<5}: {crypto_trade.crypto_amount:<10.8f}")
      print(f"   Cost Basis for each {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} pair: {cost_basis:.16f}")
      print(f"   Total Amount {usd_trade.crypto_asset}: {abs(usd_trade.total_amt):<10.2f}")
      print(f"   Crypto Fee: {crypto_trade.crypto_fee:<10.8f} {crypto_trade.crypto_asset}")
      print(f"   USD Equivalent: {usd_fee_equivalent:<10.9f}")
    
      self.wallets[usd_trade.crypto_asset] += usd_trade.crypto_amount
      self.wallets[crypto_trade.crypto_asset] += crypto_trade.crypto_amount
    
      # Check and reset wallet balances if they go negative
      for asset in [usd_trade.crypto_asset, crypto_trade.crypto_asset]:
        if self.wallets[asset] < 0:
            self.wallets[asset] = 0
    
      print(f"   {usd_trade.crypto_asset:<5} Wallet balance: {self.wallets[usd_trade.crypto_asset]:<10.8f}")
      print(f"   {crypto_trade.crypto_asset:<5} Wallet balance: {self.wallets[crypto_trade.crypto_asset]:<10.8f}")

      if crypto_trade.is_buy:
        self.positions[crypto_trade.crypto_asset].append((crypto_trade.actual_crypto_amount, cost_basis))
        self.cash_balance -= abs(usd_trade.total_amt)
      else:
        self.sell(crypto_trade, abs(usd_trade.total_amt))
        self.cash_balance += abs(usd_trade.total_amt)

      # Check and reset cash balance if it goes negative
      if self.cash_balance < 0:
        self.cash_balance = 0

      self.total_fees += crypto_trade.crypto_fee * cost_basis


    # def process_trade_pair(self, usd_trade, crypto_trade):
    #     self.line_number += 1
    #     cost_basis = abs(usd_trade.total_amt / crypto_trade.crypto_amount)
    #     usd_fee_equivalent = abs(crypto_trade.crypto_fee * cost_basis)
        
    #     print(f"----------------------------------------")
    #     print(f"{self.line_number:<3}")
    #     print(f"...Processing trade pair for {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} linked by {usd_trade.refid}")
    #     print(f"   Date: {usd_trade.date}")
    #     print(f"   Action: Pairing transaction")
    #     print(f"   {usd_trade.crypto_asset:<5}: {abs(usd_trade.crypto_amount):<10.8f}")
    #     print(f"   {crypto_trade.crypto_asset:<5}: {crypto_trade.crypto_amount:<10.8f}")
    #     print(f"   Cost Basis for each {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} pair: {cost_basis:.16f}")
    #     print(f"   Total Amount {usd_trade.crypto_asset}: {abs(usd_trade.total_amt):<10.2f}")
    #     print(f"   Crypto Fee: {crypto_trade.crypto_fee:<10.8f} {crypto_trade.crypto_asset}")
    #     print(f"   USD Equivalent: {usd_fee_equivalent:<10.9f}")
        
    #     self.wallets[usd_trade.crypto_asset] += usd_trade.crypto_amount
    #     self.wallets[crypto_trade.crypto_asset] += crypto_trade.crypto_amount
        
    #     print(f"   {usd_trade.crypto_asset:<5} Wallet balance: {self.wallets[usd_trade.crypto_asset]:<10.8f}")
    #     print(f"   {crypto_trade.crypto_asset:<5} Wallet balance: {self.wallets[crypto_trade.crypto_asset]:<10.8f}")

    #     if crypto_trade.is_buy:
    #         self.positions[crypto_trade.crypto_asset].append((crypto_trade.actual_crypto_amount, cost_basis))
    #         self.cash_balance -= abs(usd_trade.total_amt)
    #     else:
    #         self.sell(crypto_trade, abs(usd_trade.total_amt))
    #         self.cash_balance += abs(usd_trade.total_amt)

    #     self.total_fees += crypto_trade.crypto_fee * cost_basis

    def process_trade(self, trade):
        self.line_number += 1
        trade.print_trade(self.line_number)

        if trade.crypto_asset == 'USD':
            self.cash_balance += trade.crypto_amount
        elif trade.is_buy:
            if abs(trade.total_amt) <= self.cash_balance:
                self.buy(trade)
            else:
                print(f"WARNING: Insufficient funds to buy {trade.crypto_asset}. Skipping trade.")
        else:
            self.sell(trade)

    def buy(self, trade):
        cost_basis = abs(trade.total_amt) / trade.actual_crypto_amount if trade.actual_crypto_amount != 0 else 0.0
        self.positions[trade.crypto_asset].append((trade.actual_crypto_amount, cost_basis))
        self.cash_balance -= abs(trade.total_amt)
        self.total_fees += trade.crypto_fee
        
        print(f"DEBUG: Buy {trade.crypto_asset}: Amount: {trade.actual_crypto_amount}, Cost Basis: {cost_basis:.4f}, Cash Balance: {self.cash_balance:.2f}")

    def sell(self, trade):
        sell_quantity = abs(trade.crypto_amount)
        asset_queue = self.positions[trade.crypto_asset]
        total_profit = 0.0

        while sell_quantity > 0 and asset_queue:
            oldest_trade = asset_queue[0]
            if oldest_trade[0] <= sell_quantity:
                sell_quantity -= oldest_trade[0]
                buy_price = oldest_trade[1]
                sell_price = abs(trade.total_amt) / abs(trade.crypto_amount)
                profit = (sell_price - buy_price) * oldest_trade[0]
                total_profit += profit
                asset_queue.popleft()
            else:
                buy_price = oldest_trade[1]
                sell_price = abs(trade.total_amt) / abs(trade.crypto_amount)
                profit = (sell_price - buy_price) * sell_quantity
                total_profit += profit
                asset_queue[0] = (oldest_trade[0] - sell_quantity, buy_price)
                sell_quantity = 0

        if sell_quantity > 0:
            print(f"Warning: Attempted to sell more {trade.crypto_asset} than available")

        self.pnl[trade.crypto_asset] += total_profit
        self.cash_balance += abs(trade.total_amt)

        print(f"DEBUG: Sell {trade.crypto_asset}: Quantity Sold: {abs(trade.crypto_amount)}, Total Profit: {total_profit:.2f}, Cash Balance: {self.cash_balance:.2f}")

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
