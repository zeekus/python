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

 Use case download a export of your crypto transactions from Kraken in cvs format.
 rename the ledger.csv to your_csv_file.csv or update the code to user your file name.
"""

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
        if self.is_buy:
            print(f'   Buying {self.actual_crypto_amount:<10.8f} {self.crypto_asset} at {price:<10.2f} USD each for a total of {abs(self.usd_amount):<10.2f} USD')
        else:
            print(f'   Selling {abs(self.crypto_amount):<10.8f} {self.crypto_asset} at {price:<10.2f} USD each for a total of {abs(self.usd_amount):<10.2f} USD')
