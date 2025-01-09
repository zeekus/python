
# filename: Trade.py
# Description: Processes Trades.
# Copyright (C) 2025 Theodore Knab
# Special thanks to Michael von den Driesch who provided the FIFO logic
# Also Special thanks to ChatGPT
class Trade:
    def __init__(self, date, crypto_asset, crypto_amount, total_amt, crypto_fee, usd_fee, crypto_balance, txid, refid):
        self.date = date
        self.crypto_asset = crypto_asset
        self.crypto_amount = crypto_amount
        self.total_amt = total_amt  # Renamed from usd_amount to total_amt
        self.crypto_fee = crypto_fee
        self.usd_fee = usd_fee
        self.txid = txid
        self.refid = refid  # Added refid for querying FIAT wallet
        self.is_buy = crypto_amount > 0
        self.actual_crypto_amount = crypto_amount - crypto_fee if self.is_buy else crypto_amount
        self.crypto_balance = self.actual_crypto_amount if self.is_buy else crypto_balance
        self.fiat_equivalent = None  # To be set later by querying FIAT wallet

    def set_fiat_equivalent(self, fiat_amount):
        self.fiat_equivalent = fiat_amount

    def print_trade(self, line_number):
        action = "Buying" if self.is_buy else "Selling"
        price = abs(self.fiat_equivalent / self.crypto_amount) if self.crypto_amount != 0 else 0.0
        
        print(f"----------------------------------------")
        print(f'{line_number:<3}')
        print(f'...Processing trade for {self.crypto_asset:<5}/USD {self.txid}')
        print(f'   Date: {self.date}')
        print(f'   Action: {action:<6}')
        print(f'   {self.crypto_asset:<5}: {abs(self.crypto_amount):<10.8f}')
        print(f'   Total Amount: {abs(self.total_amt):<10.2f}')
        print(f'   FIAT Equivalent: {abs(self.fiat_equivalent):<10.2f}')
        print(f'   Price: {price:<10.2f} USD per {self.crypto_asset}')
        print(f'   Crypto Fee: {self.crypto_fee:<10.8f} {self.crypto_asset}')
        print(f'   USD Fee: {self.usd_fee:<10.2f} USD')
        print(f'   {self.crypto_asset:<5} Balance: {self.crypto_balance:<10.8f}')
