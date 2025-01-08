import pandas as pd
from collections import deque

class Trade:
    def __init__(self, date, asset, amount, fee, balance, amount_usd):
        self.date = date
        self.asset = asset
        self.amount = amount
        self.fee = fee
        self.balance = balance
        self.amount_usd = amount_usd
        self.is_sell = amount < 0 or amount_usd < 0

    def print_trade(self, line_number):
        action = "Selling" if self.is_sell else "Buying"
        print(f'{line_number}. Processing trade for {self.asset}')
        print(f'   Date: {self.date}')
        print(f'   Action: {action}')
        print(f'   Amount: {abs(self.amount):.8f} {self.asset}')
        print(f'   USD Value: ${abs(self.amount_usd):.2f}')
        print(f'   Fee: ${self.fee:.6f}')
        print(f'   Balance: {self.balance:.8f} {self.asset}')

class FifoAccount:
    def __init__(self):
        self.positions = {}
        self.pnl = {}
        self.cash_balance = 0
        self.line_number = 0

    def process_trade(self, trade):
        self.line_number += 1
        trade.print_trade(self.line_number)

        if trade.asset not in self.positions:
            self.positions[trade.asset] = deque()
        if trade.asset not in self.pnl:
            self.pnl[trade.asset] = 0

        if trade.is_sell:
            self.sell(trade)
        else:
            self.buy(trade)

    def buy(self, trade):
        self.positions[trade.asset].append(trade)
        if trade.asset != 'USD':
            self.cash_balance -= abs(trade.amount_usd)

    def sell(self, trade):
        if trade.asset != 'USD':
            sell_quantity = abs(trade.amount)
            asset_queue = self.positions[trade.asset]
            self.cash_balance += abs(trade.amount_usd)

            while sell_quantity > 0 and asset_queue:
                oldest_trade = asset_queue[0]
                if oldest_trade.amount <= sell_quantity:
                    sell_quantity -= oldest_trade.amount
                    profit = (abs(trade.amount_usd) / abs(trade.amount) - abs(oldest_trade.amount_usd) / abs(oldest_trade.amount)) * oldest_trade.amount
                    self.pnl[trade.asset] += profit
                    print(f'   Sold {oldest_trade.amount:.8f} {trade.asset} bought at ${abs(oldest_trade.amount_usd) / abs(oldest_trade.amount):.8f}. Profit: ${profit:.8f}')
                    asset_queue.popleft()
                else:
                    profit = (abs(trade.amount_usd) / abs(trade.amount) - abs(oldest_trade.amount_usd) / abs(oldest_trade.amount)) * sell_quantity
                    self.pnl[trade.asset] += profit
                    print(f'   Sold {sell_quantity:.8f} {trade.asset} bought at ${abs(oldest_trade.amount_usd) / abs(oldest_trade.amount):.8f}. Profit: ${profit:.8f}')
                    oldest_trade.amount -= sell_quantity
                    sell_quantity = 0

            if sell_quantity > 0:
                print(f"   Warning: Attempted to sell more {trade.asset} than available")

    def print_positions(self):
        print("\nCurrent Positions:")
        for asset, queue in self.positions.items():
            total_quantity = sum(trade.amount for trade in queue)
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

# Process each trade
for _, row in df.iterrows():
    if row['type'] == 'trade':
        date = pd.to_datetime(row['time'])
        asset = row['asset']
        amount = float(row['amount'])
        fee = float(row['fee'])
        balance = float(row['balance'])
        amount_usd = float(row['amountusd'])

        trade = Trade(date, asset, amount, fee, balance, amount_usd)
        fifo_account.process_trade(trade)

# Print final positions, cash balance, and PnL
fifo_account.print_positions()
fifo_account.print_cash_balance()
fifo_account.print_pnl()

