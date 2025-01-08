import pandas as pd
from collections import deque

class Trade:
    def __init__(self, date, base_asset, quote_asset, base_amount, quote_amount, fee, balance):
        self.date = date
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.base_amount = base_amount
        self.quote_amount = quote_amount
        self.fee = fee
        self.balance = balance
        self.is_sell = base_amount < 0 if base_asset != 'USD' else quote_amount > 0

    def print_trade(self, line_number):
        action = "Selling" if self.is_sell else "Buying"
        print(f'{line_number}. Processing trade for {self.quote_asset}/{self.base_asset}')
        print(f'   Date: {self.date}')
        print(f'   Action: {action}')
        print(f'   {self.quote_asset}: {abs(self.quote_amount):.8f}')
        print(f'   {self.base_asset}: {abs(self.base_amount):.8f}')
        print(f'   Price: {abs(self.quote_amount / self.base_amount):.8f} {self.quote_asset}')
        print(f'   Fee: ${self.fee:.6f}')
        print(f'   Balance: {self.balance:.8f} {self.base_asset}')
        if self.is_sell:
            print(f'   Selling {abs(self.base_amount):.8f} {self.base_asset} at {abs(self.quote_amount / self.base_amount):.8f} {self.quote_asset} each for a total of {abs(self.quote_amount):.8f} {self.quote_asset}')
        else:
            print(f'   Buying {abs(self.base_amount):.8f} {self.base_asset} at {abs(self.quote_amount / self.base_amount):.8f} {self.quote_asset} each for a total of {abs(self.quote_amount):.8f} {self.quote_asset}')

class FifoAccount:
    def __init__(self):
        self.positions = {}
        self.pnl = {}
        self.cash_balance = 0
        self.line_number = 0

    def process_trade(self, trade):
        self.line_number += 1
        trade.print_trade(self.line_number)

        if trade.base_asset not in self.positions:
            self.positions[trade.base_asset] = deque()
        if trade.base_asset not in self.pnl:
            self.pnl[trade.base_asset] = 0

        if trade.is_sell:
            self.sell(trade)
        else:
            self.buy(trade)

    def buy(self, trade):
        self.positions[trade.base_asset].append(trade)
        self.cash_balance -= abs(trade.quote_amount)

    def sell(self, trade):
        sell_quantity = abs(trade.base_amount)
        asset_queue = self.positions[trade.base_asset]
        self.cash_balance += abs(trade.quote_amount)

        while sell_quantity > 0 and asset_queue:
            oldest_trade = asset_queue[0]
            if oldest_trade.base_amount <= sell_quantity:
                sell_quantity -= oldest_trade.base_amount
                profit = (abs(trade.quote_amount / trade.base_amount) - abs(oldest_trade.quote_amount / oldest_trade.base_amount)) * oldest_trade.base_amount
                self.pnl[trade.base_asset] += profit
                print(f'   Sold {oldest_trade.base_amount:.8f} {trade.base_asset} bought at {abs(oldest_trade.quote_amount / oldest_trade.base_amount):.8f}. Profit: {profit:.8f} {trade.quote_asset}')
                asset_queue.popleft()
            else:
                profit = (abs(trade.quote_amount / trade.base_amount) - abs(oldest_trade.quote_amount / oldest_trade.base_amount)) * sell_quantity
                self.pnl[trade.base_asset] += profit
                print(f'   Sold {sell_quantity:.8f} {trade.base_asset} bought at {abs(oldest_trade.quote_amount / oldest_trade.base_amount):.8f}. Profit: {profit:.8f} {trade.quote_asset}')
                oldest_trade.base_amount -= sell_quantity
                sell_quantity = 0

        if sell_quantity > 0:
            print(f"   Warning: Attempted to sell more {trade.base_asset} than available")

    def print_positions(self):
        print("\nCurrent Positions:")
        for asset, queue in self.positions.items():
            total_quantity = sum(trade.base_amount for trade in queue)
            if total_quantity > 0:
                print(f"{asset}: {total_quantity:.8f}")

    def print_cash_balance(self):
        print(f"\nCurrent Cash Balance: ${self.cash_balance:.4f}")

    def print_pnl(self):
        print("\nProfit/Loss per Asset:")
        for asset, profit in self.pnl.items():
            print(f"{asset}: ${profit:.8f}")
        print(f"Total PnL: ${sum(self.pnl.values()):.8f}")

# Read the CSV file
df = pd.read_csv('your_csv_file.csv', sep='\t', quotechar='"')

# Initialize the FIFO account
fifo_account = FifoAccount()

# Process trades in pairs
for i in range(0, len(df), 2):
    if i + 1 < len(df):
        row1 = df.iloc[i]
        row2 = df.iloc[i + 1]

        #debug trade processing
        if row1['type'] == 'trade' and row2['type'] == 'trade':
            date = pd.to_datetime(row1['time'])
            quote_asset = row1['asset']
            base_asset = row2['asset']
            quote_amount = float(row1['amount'])
            print(f'debug1: quote_amount: {quote_amount}')
            base_amount = float(row2['amount'])
            print(f'debug2: base_amount: {base_amount}')
            fee = float(row2['fee'])
            balance = float(row2['balance'])
            print(f'debug3: balance: {balance}')

            trade = Trade(date, base_asset, quote_asset, base_amount, quote_amount, fee, balance)
            fifo_account.process_trade(trade)

# Print final positions, cash balance, and PnL
fifo_account.print_positions()
fifo_account.print_cash_balance()
fifo_account.print_pnl()

