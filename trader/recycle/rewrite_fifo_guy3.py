import pandas as pd
from collections import deque

class Trade:
    def __init__(self, date, quantity, price, asset, balance):
        self.date = date
        self.quantity = quantity
        self.price = price
        self.asset = asset
        self.balance = balance

    def print_trade(self):
        print(f'Date: {self.date}, Asset: {self.asset}, Quantity: {self.quantity:.8f}, Price: ${self.price:.4f}, Balance: {self.balance:.8f}')

class FifoAccount:
    def __init__(self):
        self.positions = {}
        self.pnl = {}
        self.balances = {}

    def process_trade(self, trade):
        print(f"\nProcessing trade for {trade.asset}")
        trade.print_trade()

        if trade.asset not in self.positions:
            self.positions[trade.asset] = deque()
        if trade.asset not in self.pnl:
            self.pnl[trade.asset] = 0
        
        self.balances[trade.asset] = trade.balance

        if trade.quantity > 0:
            self.buy(trade)
        elif trade.quantity < 0:
            self.sell(trade)

    def buy(self, trade):
        print(f'Buying {trade.quantity} {trade.asset} at ${trade.price:.4f}')
        self.positions[trade.asset].append(trade)

    def sell(self, trade):
        print(f'Selling {abs(trade.quantity)} {trade.asset} at ${trade.price:.4f}')
        sell_quantity = abs(trade.quantity)
        asset_queue = self.positions[trade.asset]

        while sell_quantity > 0 and asset_queue:
            oldest_trade = asset_queue[0]
            if oldest_trade.quantity <= sell_quantity:
                sell_quantity -= oldest_trade.quantity
                profit = (trade.price - oldest_trade.price) * oldest_trade.quantity
                self.pnl[trade.asset] += profit
                print(f'Sold {oldest_trade.quantity} {trade.asset} bought at ${oldest_trade.price:.4f}. Profit: ${profit:.4f}')
                asset_queue.popleft()
            else:
                profit = (trade.price - oldest_trade.price) * sell_quantity
                self.pnl[trade.asset] += profit
                print(f'Sold {sell_quantity} {trade.asset} bought at ${oldest_trade.price:.4f}. Profit: ${profit:.4f}')
                oldest_trade.quantity -= sell_quantity
                sell_quantity = 0

        if sell_quantity > 0:
            print(f"Warning: Attempted to sell more {trade.asset} than available")

    def print_positions(self):
        print("\nCurrent Positions:")
        for asset, queue in self.positions.items():
            total_quantity = sum(trade.quantity for trade in queue)
            if total_quantity > 0:
                print(f"{asset}: {total_quantity:.8f}")

    def print_balances(self):
        print("\nCurrent Balances:")
        for asset, balance in self.balances.items():
            print(f"{asset}: {balance:.8f}")

    def print_pnl(self):
        print("\nProfit/Loss per Asset:")
        for asset, profit in self.pnl.items():
            print(f"{asset}: ${profit:.2f}")
        print(f"Total PnL: ${sum(self.pnl.values()):.2f}")

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
        balance = float(row['balance'])
        
        if quantity != 0:  # Skip rows with zero quantity
            price = abs(float(row['amountusd'])) / abs(quantity)
            
            trade = Trade(date, quantity, price, asset, balance)
            fifo_account.process_trade(trade)

# Print final positions, balances, and PnL
fifo_account.print_positions()
fifo_account.print_balances()
fifo_account.print_pnl()

