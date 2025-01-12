# filename: Trade.py

# Description: Processes Trades.

# Copyright (C) 2025 Theodore Knab
# Special thanks to Michael von den Driesch who provided the FIFO logic
# Also Special thanks to ChatGPT

# This file is just a simple implementation of a python class allowing for FIFO bookkeeping

# This is free software: you can redistribute it and/or modify it
# under the terms of the BSD-2-Clause (https://opensource.org/licenses/bsd-license.html).

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the license for more details.

class Trade:
    def __init__(self, date, crypto_asset, crypto_amount, total_amt,
                 crypto_fee, usd_fee, crypto_balance, txid, refid):
        self.date = date
        self.crypto_asset = crypto_asset
        self.crypto_amount = float(crypto_amount)
        self.total_amt = float(total_amt)
        self.crypto_fee = float(crypto_fee)
        self.usd_fee = float(usd_fee)
        self.txid = txid
        self.refid = refid
        self.is_buy = (self.crypto_amount > 0)

        # For convenience, net crypto amount if it's a buy
        self.actual_crypto_amount = (
            self.crypto_amount - self.crypto_fee
            if self.is_buy else
            self.crypto_amount
        )

        # The exchange-provided “balance” after this trade, if relevant
        self.crypto_balance = float(crypto_balance)

    def print_trade(self, line_number):
        action = "Buying" if self.is_buy else "Selling"
        price = abs(self.total_amt / self.crypto_amount) if self.crypto_amount != 0 else 0.0
        print(f"----------------------------------------")
        print(f'{line_number:<3}')
        print(f'...Processing trade for {self.crypto_asset:<5}/USD {self.txid}')
        print(f' Date: {self.date}')
        print(f' Action: {action:<6}')
        print(f' {self.crypto_asset:<5}: {abs(self.crypto_amount):<10.8f}')
        print(f' Total Amount: {abs(self.total_amt):<10.2f}')
        print(f' Price: {price:<10.4f} USD per {self.crypto_asset}')
        print(f' Crypto Fee: {self.crypto_fee:<10.8f} {self.crypto_asset}')
        print(f' USD Fee: {self.usd_fee:<10.2f} USD')
        print(f' {self.crypto_asset:<5} Balance: {self.crypto_balance:<10.8f}')

