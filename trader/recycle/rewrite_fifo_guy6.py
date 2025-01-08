import pandas as pd
from collections import deque

class Trade:
    def __init__(self, date, quantity, price, asset, cash_balance, fee):
        self.date = date
        self.quantity = quantity
        self.price = price
        self.asset = asset
        self.cash_balance = cash_balance
        self.fee = fee

    def print_trade(self, line_number):
        print(f'{line_number}. Date: {self.date}, Asset: {self.asset}, Quantity: {self.quantity:.8f}, Price: ${self.price:.6f}, Cash Balance: ${self.cash_balance:.4f}, Fee: ${self.fee:.6f}')

class FifoAccount:
    def __init__(self):
        self.positions = {}
        self.pnl = {}
        self.cash_balance = 0
        self.line_number = 0

    def process_trade(self, trade):
        self.line_number += 1
        print(f"\n{self.line_number}. Processing trade for {trade.asset}")
        trade.print_trade(self.line_number)

        self.cash_balance = trade.cash_balance

        if trade.asset != 'USD':
            if trade.asset not in self.positions:
                self.positions[trade.asset] = deque()
            if trade.asset not in self.pnl:
                self.pnl[trade.asset] = 0

            if trade.quantity > 0:
                self.buy(trade)
            elif trade.quantity < 0:
                self.sell(trade)

    def buy(self, trade):
        self.line_number += 1
        print(f'{self.line_number}. Buying {trade.quantity} {trade.asset} at ${trade.price:.6f}')
        self.positions[trade.asset].append(trade)

    def sell(self, trade):
        self.line_number += 1
        print(f'{self.line_number}. Selling {abs(trade.quantity)} {trade.asset} at ${trade.price:.6f}')
        sell_quantity = abs(trade.quantity)
        asset_queue = self.positions[trade.asset]

        while sell_quantity > 0 and asset_queue:
            oldest_trade = asset_queue[0]
            if oldest_trade.quantity <= sell_quantity:
                sell_quantity -= oldest_trade.quantity
                profit = (trade.price - oldest_trade.price) * oldest_trade.quantity
                self.pnl[trade.asset] += profit
                self.line_number += 1
                print(f'{self.line_number}. Sold {oldest_trade.quantity} {trade.asset} bought at ${oldest_trade.price:.6f}. Profit: ${profit:.6f}')
                asset_queue.popleft()
            else:
                profit = (trade.price - oldest_trade.price) * sell_quantity
                self.pnl[trade.asset] += profit
                self.line_number += 1
                print(f'{self.line_number}. Sold {sell_quantity} {trade.asset} bought at ${oldest_trade.price:.6f}. Profit: ${profit:.6f}')
                oldest_trade.quantity -= sell_quantity
                sell_quantity = 0

        if sell_quantity > 0:
            self.line_number += 1
            print(f"{self.line_number}. Warning: Attempted to sell more {trade.asset} than available")

    def print_positions(self):
        self.line_number += 1
        print(f"\n{self.line_number}. Current Positions:")
        for asset, queue in self.positions.items():
            total_quantity = sum(trade.quantity for trade in queue)
            if total_quantity > 0:
                self.line_number += 1
                print(f"{self.line_number}. {asset}: {total_quantity:.8f}")

    def print_cash_balance(self):
        self.line_number += 1
        print(f"\n{self.line_number}. Current Cash Balance: ${self.cash_balance:.4f}")

    def print_pnl(self):
        self.line_number += 1
        print(f"\n{self.line_number}. Profit/Loss per Asset:")
        for asset, profit in self.pnl.items():
            self.line_number += 1
            print(f"{self.line_number}. {asset}: ${profit:.6f}")
        self.line_number += 1
        print(f"{self.line_number}. Total PnL: ${sum(self.pnl.values()):.6f}")

# Read the CSV file
df = pd.read_csv('your_csv_file.csv', sep='\t', quotechar='"')

# Initialize the FIFO account
fifo_account = FifoAccount()

# Process each trade
for _, row in df.iterrows():
    if row['type'] == 'trade':
        date = pd.to_datetime(row['time'])
        asset = row['asset']
        quantity = float(row['amount'])
        fee = float(row['fee'])
        
        if asset == 'USD':
            cash_balance = float(row['balance'])
            price = 1.0  # USD price is always 1
        else:
            cash_balance = fifo_account.cash_balance
            price = abs(float(row['amountusd'])) / (abs(quantity) + fee)  # Include fee in price calculation
        
        if quantity != 0:  # Skip rows with zero quantity
            trade = Trade(date, quantity, price, asset, cash_balance, fee)
            fifo_account.process_trade(trade)

# Print final positions, cash balance, and PnL
fifo_account.print_positions()
fifo_account.print_cash_balance()
fifo_account.print_pnl()

