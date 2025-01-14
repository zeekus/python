# FifoAccount.py
# Description: Holds and runs FIFO logic for buys/sells
# Copyright (C) 2025 Theodore Knab
# Special thanks to Michael von den Driesch who provided the FIFO logic
# Also Special thanks to ChatGPT
# This file is just a simple implementation of a python class allowing for FIFO bookkeeping 
#
# This is free software: you can redistribute it and/or modify it
# under the terms of the BSD-2-Clause (https://opensource.org/licenses/bsd-license.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the license for more details.

from collections import defaultdict, deque

class FifoAccount:
    def __init__(self):
        self.positions = defaultdict(deque)
        self.pnl = defaultdict(float)
        self.cash_balance = 0.0
        self.total_fees = 0.0
        self.line_number = 0
        self.wallets = defaultdict(float)
        self.closed_trades = 0  # New attribute to track closed trades

    def process_trade_pair(self, usd_trade, crypto_trade):
        self.line_number += 1
        if crypto_trade.crypto_amount == 0:
            print(f"Warning: Zero crypto amount for {crypto_trade.crypto_asset} trade.")
            return

        sell_price = abs(usd_trade.total_amt / crypto_trade.crypto_amount)
        usd_fee_equivalent = abs(crypto_trade.crypto_fee * sell_price)

        print(f"----------------------------------------")
        print(f"{self.line_number:<3}")
        print(f'...Debug: process_trade_pair function')
        print(f"...Processing trade pair for {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} linked by {usd_trade.refid}")
        print(f" Date: {usd_trade.date}")
        print(f" Action: {'Buy' if crypto_trade.is_buy else 'Sell'}")
        print(f" {usd_trade.crypto_asset:<5}: {abs(usd_trade.crypto_amount):<10.8f}")
        print(f" {crypto_trade.crypto_asset:<5}: {abs(crypto_trade.crypto_amount):<10.8f}")
        print(f" Price for each {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} pair: {sell_price:.16f}")
        print(f" Total Amount {usd_trade.crypto_asset}: {abs(usd_trade.total_amt):<10.2f}")
        print(f" Crypto Fee: {crypto_trade.crypto_fee:<10.8f} {crypto_trade.crypto_asset}")
        print(f" USD Equivalent: {usd_fee_equivalent:<10.9f}")

        # Update wallet balances considering fees
        if crypto_trade.is_buy:
            actual_crypto_amount = abs(crypto_trade.crypto_amount) - crypto_trade.crypto_fee
            self.wallets[usd_trade.crypto_asset] += usd_trade.crypto_amount
            self.wallets[crypto_trade.crypto_asset] += actual_crypto_amount
        else:
            self.wallets[usd_trade.crypto_asset] += usd_trade.crypto_amount
            self.wallets[crypto_trade.crypto_asset] -= abs(crypto_trade.crypto_amount) + crypto_trade.crypto_fee

        # Check if the wallet balance has gone to 0.0
        if abs(self.wallets[crypto_trade.crypto_asset]) <= 1e-10:
            self.closed_trades += 1
            print(f"Fully Executed Trades: {self.closed_trades}")

        if self.wallets[usd_trade.crypto_asset] < 0:
            self.wallets[usd_trade.crypto_asset] = 0

        print(f" {usd_trade.crypto_asset:<5} Wallet balance: {self.wallets[usd_trade.crypto_asset]:<10.8f}")
        print(f" {crypto_trade.crypto_asset:<5} Wallet balance: {self.wallets[crypto_trade.crypto_asset]:<10.8f}")

        if crypto_trade.is_buy:
            actual_crypto_amount = abs(crypto_trade.crypto_amount) - crypto_trade.crypto_fee
            self.positions[crypto_trade.crypto_asset].append((actual_crypto_amount, sell_price, usd_fee_equivalent))
            self.cash_balance -= abs(usd_trade.total_amt)
        else:
            self.sell(crypto_trade, sell_price, usd_fee_equivalent)
            self.cash_balance += abs(usd_trade.total_amt)

        self.total_fees += usd_fee_equivalent


    def process_single_trade(self, trade):
         self.line_number += 1
         if trade.crypto_asset == 'USD':
            self.cash_balance += trade.crypto_amount
         elif trade.is_buy:
            self.buy(trade)
         else:
            sell_price = abs(trade.total_amt / trade.crypto_amount) if trade.crypto_amount != 0 else 0.0
            self.sell(trade, sell_price, trade.usd_fee)

         print(f"----------------------------------------")
         print(f"{self.line_number:<3}")
         print(f'...Debug: process_single_trade')
         print(f"...Processing trade for {trade.crypto_asset}")
         print(f" Date: {trade.date}")
         print(f" Action: {'Buy' if trade.is_buy else 'Sell'}")
         print(f" {trade.crypto_asset:<5}: {abs(trade.crypto_amount):<10.8f}")
         print(f" Total Amount: {abs(trade.total_amt):<10.2f}")
         print(f" Crypto Fee: {trade.crypto_fee:<10.8f} {trade.crypto_asset}")

         # Update wallet balances considering fees
         if trade.is_buy:
            actual_crypto_amount = abs(trade.crypto_amount) - trade.crypto_fee
            self.wallets[trade.crypto_asset] += actual_crypto_amount
         else:
            self.wallets[trade.crypto_asset] -= abs(trade.crypto_amount) + trade.crypto_fee

         if trade.crypto_asset == 'USD' and self.wallets[trade.crypto_asset] < 0:
            self.wallets[trade.crypto_asset] = 0

         print(f" {trade.crypto_asset:<5} Wallet balance: {self.wallets[trade.crypto_asset]:<10.8f}")

    def buy(self, trade):
        cost_basis = abs(trade.total_amt) / abs(trade.crypto_amount) if trade.crypto_amount != 0 else 0.0
        actual_crypto_amount = abs(trade.crypto_amount) - trade.crypto_fee
        self.positions[trade.crypto_asset].append((actual_crypto_amount, cost_basis, trade.usd_fee))
        self.cash_balance -= abs(trade.total_amt)
        self.total_fees += trade.usd_fee
        
        print(f"DEBUG: Buy {trade.crypto_asset}: Amount: {actual_crypto_amount}, Cost Basis: {cost_basis:.4f}, Cash Balance: {self.cash_balance:.2f}")

    def sell(self, trade, sell_price, sell_fee):
        sell_quantity = abs(trade.crypto_amount)
        asset_queue = self.positions[trade.crypto_asset]
        total_profit = 0.0

        print(f"DEBUG: Starting sell for {trade.crypto_asset}")
        print(f"DEBUG: Sell Quantity: {sell_quantity}")
        print(f"DEBUG: Sell Price: {sell_price:.2f}")
        print(f"DEBUG: Sell Fee: {sell_fee:.2f}")
        print(f"DEBUG: Initial Asset Queue: {list(asset_queue)}")

        while sell_quantity > 0 and asset_queue:
            oldest_trade = asset_queue[0]
            print(f"DEBUG: Processing oldest trade: {oldest_trade}")

            if oldest_trade[0] <= sell_quantity:
                sell_quantity -= oldest_trade[0]
                buy_price, buy_fee = oldest_trade[1], oldest_trade[2]
                profit = self.calculate_profit(oldest_trade[0], sell_price, buy_price, buy_fee, sell_fee * (oldest_trade[0] / abs(trade.crypto_amount)))
                total_profit += profit['profit']
                asset_queue.popleft()
                print(f"DEBUG: Sold full quantity of oldest trade.")
                print(f"DEBUG: Buy Price: {buy_price:.2f}, Sell Price: {sell_price:.2f}")
                print(f"DEBUG: Profit for this portion: {profit['profit']:.2f}")
                print(f"DEBUG: Remaining Sell Quantity: {sell_quantity}")
            else:
                buy_price, buy_fee = oldest_trade[1], oldest_trade[2]
                profit = self.calculate_profit(sell_quantity, sell_price, buy_price, buy_fee * (sell_quantity / oldest_trade[0]), sell_fee * (sell_quantity / abs(trade.crypto_amount)))
                total_profit += profit['profit']
                asset_queue[0] = (oldest_trade[0] - sell_quantity, buy_price, buy_fee * ((oldest_trade[0] - sell_quantity) / oldest_trade[0]))
                print(f"DEBUG: Partially sold oldest trade.")
                print(f"DEBUG: Buy Price: {buy_price:.2f}, Sell Price: {sell_price:.2f}")
                print(f"DEBUG: Profit for this portion: {profit['profit']:.2f}")
                print(f"DEBUG: Remaining in oldest trade: {asset_queue[0]}")
                sell_quantity = 0

        if sell_quantity > 0:
            print(f"Warning: Attempted to sell more {trade.crypto_asset} than available")
            print(f"DEBUG: Excess sell quantity: {sell_quantity}")

        self.pnl[trade.crypto_asset] += total_profit
        self.cash_balance += abs(trade.total_amt)
        self.total_fees += sell_fee

        print(f"DEBUG: Total Profit for this sell: {total_profit:.2f}")
        print(f"DEBUG: Updated Cash Balance: {self.cash_balance:.2f}")
        print(f"DEBUG: Updated Asset Queue: {list(asset_queue)}")
        print(f"DEBUG: Updated PNL for {trade.crypto_asset}: {self.pnl[trade.crypto_asset]:.2f}")

    def calculate_profit(self, sell_quantity, sell_price, buy_price, buy_fee, sell_fee):
        cost_basis = buy_price * sell_quantity
        sell_value = sell_price * sell_quantity
        adjusted_sell_value = sell_value - sell_fee
        adjusted_cost_basis = cost_basis + buy_fee
        profit = adjusted_sell_value - adjusted_cost_basis

        return {
            "sell_quantity": sell_quantity,
            "sell_price": sell_price,
            "buy_price": buy_price,
            "buy_fee": buy_fee,
            "sell_fee": sell_fee,
            "cost_basis": cost_basis,
            "sell_value": sell_value,
            "adjusted_cost_basis": adjusted_cost_basis,
            "adjusted_sell_value": adjusted_sell_value,
            "profit": profit
        }


    def print_pnl(self):
        total_profit = 0
        print("\nProfit/Loss per Asset:")
        print(f"------------------------------")
        for asset, profit in sorted(self.pnl.items()):
            total_profit += profit
            print(f"{asset}: ${profit:.2f}")
        print(f"Total Profit/Loss ${total_profit:.2f}")

    def print_positions(self):
       open_trades = 0
       print("\nCurrent Positions:")
       print(f"------------------------------")
       for asset, queue in sorted(self.positions.items()):
         total_quantity = sum(trade[0] for trade in queue)
         if abs(total_quantity) > 1e-10:
             # Calculate average cost basis
             total_cost = sum(trade[0] * trade[1] for trade in queue)
             avg_cost_basis = total_cost / total_quantity if total_quantity != 0 else 0
            
             print(f"{asset}: {total_quantity:.8f} (Avg Cost Basis: ${avg_cost_basis:.4f})")
             open_trades += 1
       print(f"------------------------------")
       print(f"Simple stats:")
       print(f".. Open Trades: {open_trades}")
       print(f".. Executed Trades: {self.closed_trades}")
