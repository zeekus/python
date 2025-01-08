class Trade:
    def __init__(self, date, crypto_asset, crypto_amount, usd_amount, fee, crypto_balance):
        self.date = date
        self.crypto_asset = crypto_asset
        self.crypto_amount = crypto_amount
        self.usd_amount = usd_amount
        self.fee = fee
        self.is_buy = usd_amount < 0  # Buy if USD amount is negative
        self.actual_crypto_amount = crypto_amount - fee if self.is_buy else crypto_amount
        self.crypto_balance = self.actual_crypto_amount if self.is_buy else crypto_balance

    def print_trade(self, line_number):
        action = "Buying" if self.is_buy else "Selling"
        price = abs(self.usd_amount / self.crypto_amount)
        print(f'{line_number}. Processing trade for {self.crypto_asset}/USD')
        print(f'   Date: {self.date}')
        print(f'   Action: {action}')
        print(f'   {self.crypto_asset}: {abs(self.crypto_amount):.8f}')
        print(f'   USD: {abs(self.usd_amount):.8f}')
        print(f'   Price: {price:.8f} USD per {self.crypto_asset}')
        print(f'   Fee: {self.fee:.8f} {self.crypto_asset}')
        print(f'   {self.crypto_asset} Balance: {self.crypto_balance:.8f}')
        if self.is_buy:
            print(f'   Buying {self.actual_crypto_amount:.8f} {self.crypto_asset} at {price:.8f} USD each for a total of {abs(self.usd_amount):.8f} USD')
        else:
            print(f'   Selling {abs(self.crypto_amount):.8f} {self.crypto_asset} at {price:.8f} USD each for a total of {abs(self.usd_amount):.8f} USD')

