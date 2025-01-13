# FifoAccount.py

# Description: Holds and runs FIFO logic for buys/sells in pairs,
# counting "Trade #1, #2, ..." from the time an asset's position
# is opened (0 -> buy) until it is closed (final sell -> 0).

# Copyright (C) 2025 Theodore Knab
# Special thanks to Michael von den Driesch who provided the FIFO logic
# Also Special thanks to ChatGPT

# This file is just a simple implementation of a python class allowing for FIFO bookkeeping

# This is free software: you can redistribute it and/or modify it
# under the terms of the BSD-2-Clause (https://opensource.org/licenses/bsd-license.html).

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the license for more details.

from collections import defaultdict, deque
from datetime import datetime
from utils import format_trade_runtime  # so we can compute trade durations

class FifoAccount:
    def __init__(self):
        # For each crypto asset, we store a queue of FIFO positions:
        # (quantity, cost_basis, buy_fee, open_date, trade_number)
        self.positions = defaultdict(deque)

        self.pnl = defaultdict(float)
        self.cash_balance = 0.0
        self.total_fees = 0.0

        # For console output
        self.line_number = 0

        # Wallet balances per asset
        self.wallets = defaultdict(float)

        # We'll track "Trade #X" per asset. Each time an asset goes from 0 to a positive position, we start a new trade #.
        # Once sells bring it back to 0, that trade is 'closed'. The next re-buy is a new trade # for that asset.
        self.trade_number_for_asset = defaultdict(int)
        self.trade_open_date_for_asset = {}

    def process_trade_pair(self, usd_trade, crypto_trade):
        """
        Handle a matched USD+crypto transaction from the same refid.
        We'll detect if it's a buy or sell by checking crypto_trade.is_buy.
        """
        self.line_number += 1
        print("----------------------------------------")
        print(f"{self.line_number:<3}")
        print('...Debug: process_trade_pair')
        print(f"...Processing trade pair for {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} linked by {usd_trade.refid}")

        if abs(crypto_trade.crypto_amount) < 1e-12:
            print(f"Warning: Zero crypto amount for {crypto_trade.crypto_asset}. Skipping.")
            return

        # price in USD per 1 unit of crypto
        price_each = abs(usd_trade.total_amt / crypto_trade.crypto_amount) if crypto_trade.crypto_amount != 0 else 0.0
        usd_fee_equiv = abs(crypto_trade.crypto_fee * price_each)

        # Update wallet
        self.wallets[usd_trade.crypto_asset] += usd_trade.crypto_amount
        # If it's a buy, we add net (crypto_amount - fee). If it's a sell, we add negative crypto_amount
        if crypto_trade.is_buy:
            self.wallets[crypto_trade.crypto_asset] += (crypto_trade.crypto_amount - crypto_trade.crypto_fee)
        else:
            self.wallets[crypto_trade.crypto_asset] += crypto_trade.crypto_amount

        # Protect from tiny negative rounding
        if self.wallets[usd_trade.crypto_asset] < 0:
            self.wallets[usd_trade.crypto_asset] = 0

        # Print the summary
        print(f"   Date: {usd_trade.date}")
        print(f"   Action: {'Buy' if crypto_trade.is_buy else 'Sell'}")
        print(f"   {usd_trade.crypto_asset:<5}: {abs(usd_trade.crypto_amount):.8f}")
        print(f"   {crypto_trade.crypto_asset:<5}: {abs(crypto_trade.crypto_amount):.8f}")
        print(f"   Price for each {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} pair: {price_each:.16f}")
        print(f"   Total Amount {usd_trade.crypto_asset}: {abs(usd_trade.total_amt):.2f}")
        print(f"   Crypto Fee: {crypto_trade.crypto_fee:.8f} {crypto_trade.crypto_asset}")
        print(f"   USD Equivalent: {usd_fee_equiv:.9f}")
        print(f"   {usd_trade.crypto_asset:<5} Wallet balance: {self.wallets[usd_trade.crypto_asset]:.8f}")
        print(f"   {crypto_trade.crypto_asset:<5} Wallet balance: {self.wallets[crypto_trade.crypto_asset]:.8f}")

        # Distinguish buy vs sell
        if crypto_trade.is_buy:
            self._process_buy(usd_trade, crypto_trade)
        else:
            self._process_sell(usd_trade, crypto_trade)

        self.total_fees += usd_fee_equiv

    def _ensure_trade_number(self, asset, date_when_buy):
        """
        If this asset's total position is near zero, we open a new trade #.
        Otherwise, we keep using the existing trade # for that asset.
        """
        position_qty = sum(pos[0] for pos in self.positions[asset])
        if abs(position_qty) < 1e-12:
            self.trade_number_for_asset[asset] += 1
            self.trade_open_date_for_asset[asset] = date_when_buy

        return self.trade_number_for_asset[asset]

    def _process_buy(self, usd_trade, crypto_trade):
        asset = crypto_trade.crypto_asset
        # Determine the trade # for this buy
        trade_num = self._ensure_trade_number(asset, crypto_trade.date)

        # Now compute net purchased
        net_crypto = abs(crypto_trade.crypto_amount) - crypto_trade.crypto_fee
        if net_crypto > 0:
            adjusted_price = abs(usd_trade.total_amt) / net_crypto
        else:
            adjusted_price = 0

        # Print extra detail lines
        print(f"   {asset}   [ After Fees removal ] Wallet Balance: {self.wallets[asset]:.10f}")
        print(f"   Price for each USD/{asset} pair [ After Removing Fees]: {adjusted_price:.16f}")
        print(f"   Trade: {trade_num}")
        print(f"   Trade Status: Open ")

        # Insert into FIFO queue
        open_date = self.trade_open_date_for_asset.get(asset, crypto_trade.date)
        self.positions[asset].append((
            net_crypto,
            adjusted_price,
            abs(crypto_trade.crypto_fee * adjusted_price),  # approximate cost in USD for the crypto fee
            open_date,
            trade_num
        ))
        self.cash_balance -= abs(usd_trade.total_amt)

    def _process_sell(self, usd_trade, crypto_trade):
        asset = crypto_trade.crypto_asset
        # If no trade # for that asset yet, force one
        if asset not in self.trade_number_for_asset:
            self.trade_number_for_asset[asset] = 1
            self.trade_open_date_for_asset[asset] = crypto_trade.date

        trade_num = self.trade_number_for_asset[asset]
        print(f"   Trade: {trade_num}")

        # Now do FIFO SELL
        self.sell(crypto_trade, trade_num)

    def sell(self, trade, trade_number):
        print(f"DEBUG: Starting sell for {trade.crypto_asset}")

        from profit_calculator import format_trade_runtime  # local import to avoid circular references

        sell_quantity = abs(trade.crypto_amount)
        sell_price = abs(trade.total_amt / trade.crypto_amount) if trade.crypto_amount != 0 else 0.0
        sell_fee = 0.0  # We already accounted for crypto fees in the wallet update
        print(f"DEBUG: Sell Quantity: {sell_quantity:.8f}")
        print(f"DEBUG: Sell Price: {sell_price:.4f}")
        print(f"DEBUG: Sell Fee: {sell_fee:.4f}")

        asset_queue = self.positions[trade.crypto_asset]
        print(f"DEBUG: Initial Asset Queue: {list(asset_queue)}")

        total_profit = 0.0
        final_sell_date = trade.date
        fully_closed = False

        while sell_quantity > 1e-12 and asset_queue:
            oldest_qty, oldest_price, oldest_fee, oldest_date, oldest_tnum = asset_queue[0]
            print(f"DEBUG: Processing oldest trade chunk => qty={oldest_qty:.8f}, price={oldest_price:.8f}, fee={oldest_fee:.8f}, trade_num={oldest_tnum}")

            if oldest_qty <= sell_quantity + 1e-12:
                # We'll sell this entire chunk
                partial_profit = self.calculate_profit(
                    oldest_qty, sell_price, oldest_price, oldest_fee, 0.0
                )
                total_profit += partial_profit
                sell_quantity -= oldest_qty
                asset_queue.popleft()

                print(f"DEBUG: Fully sold chunk of {oldest_qty:.8f}. Partial profit {partial_profit:.2f}, leftover sell {sell_quantity:.8f}")
            else:
                # partial chunk
                portion_sold = sell_quantity
                # proportion of the buy_fee
                ratio = portion_sold / oldest_qty
                partial_profit = self.calculate_profit(
                    portion_sold, sell_price, oldest_price, oldest_fee * ratio, 0.0
                )
                total_profit += partial_profit

                new_qty = oldest_qty - portion_sold
                new_fee = oldest_fee * (1 - ratio)

                asset_queue[0] = (new_qty, oldest_price, new_fee, oldest_date, oldest_tnum)

                print(f"DEBUG: Partially sold {portion_sold:.8f} from chunk of {oldest_qty:.8f}. Profit {partial_profit:.2f}")
                print(f"DEBUG: Remainder => {asset_queue[0]}")
                sell_quantity = 0

        self.pnl[trade.crypto_asset] += total_profit
        self.cash_balance += abs(trade.total_amt)

        print(f"DEBUG: Total Profit for this sell: {total_profit:.2f}")
        print(f"DEBUG: Updated Cash Balance: {self.cash_balance:.2f}")
        print(f"DEBUG: Updated Asset Queue: {list(asset_queue)}")
        print(f"DEBUG: Updated PNL for {trade.crypto_asset}: {self.pnl[trade.crypto_asset]:.2f}")

        # Check if the position is back to zero => close this trade
        if self._is_position_zero(trade.crypto_asset):
            print(f"   Trade Status: Closed [ Lot {trade_number} sold ]")
            # Show runtime
            if trade.crypto_asset in self.trade_open_date_for_asset:
                open_dt = self.trade_open_date_for_asset[trade.crypto_asset]
                runtime_str = format_trade_runtime(open_dt, final_sell_date)
                print(f"   Trade runtime: {runtime_str}")
            # Next time we buy that asset again, we open a new trade number
            del self.trade_open_date_for_asset[trade.crypto_asset]
        else:
            if sell_quantity > 1e-12:
                # theoretically we had leftover if queue was empty
                print(f"   Trade Status: Open [ partial leftover not sold? ]")
            else:
                print(f"   Trade Status: Open [ Partial Sell ]")

        print(f"   Sell Quantity: {abs(trade.crypto_amount)}")
        print(f"   Sell Price: {sell_price:.4f}")
        print(f"   Sell Fee: {sell_fee:.4f}")
        print(f"   Updated PNL for {trade.crypto_asset}: {self.pnl[trade.crypto_asset]:.2f}")

    def _is_position_zero(self, asset):
        total_qty = sum(pos[0] for pos in self.positions[asset])
        return abs(total_qty) < 1e-12

    def calculate_profit(self, sell_quantity, sell_price, buy_price, buy_fee, sell_fee):
        # cost basis
        cost_basis = buy_price * sell_quantity + buy_fee
        proceeds = sell_price * sell_quantity - sell_fee
        profit = proceeds - cost_basis
        return profit

    def process_single_trade(self, trade):
        """
        If there's a scenario with only 1 line in refid. 
        Typically for deposits or other corner cases. 
        We'll just do the naive approach or ignore it.
        """
        self.line_number += 1
        print("----------------------------------------")
        print(f"{self.line_number:<3}")
        print('...Debug: process_single_trade')
        print(f"...Single transaction for {trade.crypto_asset}, ignoring or partial logic.")
        # You can adapt if needed. For now, we won't handle single lines in a special way.

    def print_positions(self):
        print("\nCurrent Positions:")
        for asset, queue in sorted(self.positions.items()):
            total_quantity = sum(item[0] for item in queue)
            if abs(total_quantity) > 1e-12:
                print(f"{asset}: {total_quantity:.8f}")

    def print_pnl(self):
        total = 0.0
        print("\nProfit/Loss per Asset:")
        for asset, val in sorted(self.pnl.items()):
            total += val
            print(f"{asset}: ${val:.2f}")
        print(f"Total Profit/Loss: ${total:.2f}")

