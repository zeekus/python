import pandas as pd
import numpy as np
from collections import deque

class Trade:
    def __init__(self, date, asset, quantity, price):
        self.date = date
        self.asset = asset
        self.quantity = quantity
        self.price = price

    def printT(self):
        print(f'Date: {self.date}, Asset: {self.asset}, Quantity: {self.quantity}, Price: {self.price}')

class FifoAccount:
    def __init__(self):
        self._deque = deque()
        self._pnl = 0
        self._quantity = 0
        self._bookvalue = 0

    def process_trade(self, trade):
        if trade.quantity > 0:
            self.buy(trade)
        else:
            self.sell(trade)

    def buy(self, trade):
        print('Buy trade')
        trade.printT()
        self._deque.append(trade)
        self._bookvalue += trade.quantity * trade.price
        self._quantity += trade.quantity
        self.print_stat()

    def sell(self, trade):
        print('Sell trade')
        trade.printT()
        sell_quantity = abs(trade.quantity)
        while sell_quantity > 0:
            if not self._deque:
                print("Error: Attempting to sell more than available")
                return
            oldest_trade = self._deque[0]
            if oldest_trade.quantity <= sell_quantity:
                self._deque.popleft()
                self._pnl += (trade.price - oldest_trade.price) * oldest_trade.quantity
                self._quantity -= oldest_trade.quantity
                self._bookvalue -= oldest_trade.price * oldest_trade.quantity
                sell_quantity -= oldest_trade.quantity
            else:
                self._pnl += (trade.price - oldest_trade.price) * sell_quantity
                self._quantity -= sell_quantity
                self._bookvalue -= oldest_trade.price * sell_quantity
                oldest_trade.quantity -= sell_quantity
                sell_quantity = 0
        self.print_stat()

    def print_stat(self):
        print(f'Quantity: {self._quantity}, Book Value: {self._bookvalue:.2f}, PnL: {self._pnl:.2f}')

# Read CSV file
df = pd.read_csv('your_csv_file.csv', sep='\t')

# Initialize FIFO accounts for each asset
fifo_accounts = {}

# Process trades
for _, row in df.iterrows():
    asset = row['asset']
    if asset not in fifo_accounts:
        fifo_accounts[asset] = FifoAccount()

    date = pd.to_datetime(row['time'])
    quantity = float(row['amount'])
    price = abs(float(row['amountusd']) / quantity) if quantity != 0 else 0

    trade = Trade(date, asset, quantity, price)
    fifo_accounts[asset].process_trade(trade)

# Print final statistics for each asset
for asset, account in fifo_accounts.items():
    print(f"\nFinal statistics for {asset}:")
    account.print_stat()

