import pandas as pd
from collections import deque

class Trade:
    def __init__(self, date, base_asset, quote_asset, base_quantity, quote_quantity, fee):
        self.date = date
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.base_quantity = base_quantity
        self.quote_quantity = quote_quantity
        self.fee = fee
        self.price = abs(quote_quantity) / abs(base_quantity) if base_quantity != 0 else 0
        self.cost_basis = (abs(quote_quantity) + fee) / abs(base_quantity) if base_quantity != 0 else 0
        self.is_buy = quote_quantity < 0  # Buy if USD amount is negative

    def print_trade(self, line_number):
        action = "Buying" if self.is_buy else "Selling"
        print(f'{line_number}. Processing trade for {self.base_asset}/{self.quote_asset}')
        print(f'   Date: {self.date}')
        print(f'   Pair: {self.base_asset}/{self.quote_asset}')
        print(f'   Action: {action}')
        print(f'   Base Quantity: {self.base_quantity:.8f}')
        print(f'   Quote Quantity: {self.quote_quantity:.8f}')
        print(f'   Price: ${self.price:.6f}')
        print(f'   Fee: ${self.fee:.6f}')
        print(f'   Cost Basis: ${self.cost_basis:.6f}')

class FifoAccount:
    def __init__(self):
        self.positions = {}
        self.pnl = {}
        self.cash_balance = 0
        self.line_number = 0

    def process_trade(self, trade):
        self.line_number += 1
        trade.print_trade(self.line_number)

        self.cash_balance -= trade.quote_quantity  # Update cash balance

        if trade.base_asset not in self.positions:
            self.positions[trade.base_asset] = deque()
        if trade.base_asset not in self.pnl:
            self.pnl[trade.base_asset] = 0

        if trade.is_buy:
            self.buy(trade)
        else:
            self.sell(trade)

    def buy(self, trade):
        print(f'   Buying {trade.base_quantity} {trade.base_asset} at ${trade.price:.6f}')
        self.positions[trade.base_asset].append(trade)

    def sell(self, trade):
        print(f'   Selling {abs(trade.base_quantity)} {trade.base_asset} at ${trade.price:.6f}')
        sell_quantity = abs(trade.base_quantity)
        asset_queue = self.positions[trade.base_asset]

        while sell_quantity > 0 and asset_queue:
            oldest_trade = asset_queue[0]
            if oldest_trade.base_quantity <= sell_quantity:
                sell_quantity -= oldest_trade.base_quantity
                profit = (trade.price - oldest_trade.cost_basis) * oldest_trade.base_quantity
                self.pnl[trade.base_asset] += profit
                print(f'   Sold {oldest_trade.base_quantity} {trade.base_asset} bought at ${oldest_trade.cost_basis:.6f}. Profit: ${profit:.6f}')
                asset_queue.popleft()
            else:
                profit = (trade.price - oldest_trade.cost_basis) * sell_quantity
                self.pnl[trade.base_asset] += profit
                print(f'   Sold {sell_quantity} {trade.base_asset} bought at ${oldest_trade.cost_basis:.6f}. Profit: ${profit:.6f}')
                oldest_trade.base_quantity -= sell_quantity
                sell_quantity = 0

        if sell_quantity > 0:
            print(f"   Warning: Attempted to sell more {trade.base_asset} than available")

    def print_positions(self):
        print("\nCurrent Positions:")
        for asset, queue in self.positions.items():
            total_quantity = sum(trade.base_quantity for trade in queue)
            if total_quantity > 0:
                print(f"{asset}: {total_quantity:.8f}")

    def print_cash_balance(self):
        print(f"\nCurrent Cash Balance: ${self.cash_balance:.4f}")

    def print_pnl(self):
        print("\nProfit/Loss per Asset:")
        for asset, profit in self.pnl.items():
            print(f"{asset}: ${profit:.6f}")
        print(f"Total PnL: ${sum(self.pnl.values()):.6f}")

# Read the CSV file
df = pd.read_csv('your_csv_file.csv', sep='\t', quotechar='"')

# Initialize the FIFO account
fifo_account = FifoAccount()

# Process trades in pairs
for i in range(0, len(df), 2):
    if i + 1 < len(df):
        row1 = df.iloc[i]
        row2 = df.iloc[i + 1]

        if row1['type'] == 'trade' and row2['type'] == 'trade':
            date = pd.to_datetime(row1['time'])
            base_asset = row2['asset']
            quote_asset = row1['asset']
            base_quantity = float(row2['amount'])
            quote_quantity = float(row1['amount'])
            fee = float(row2['fee'])

            trade = Trade(date, base_asset, quote_asset, base_quantity, quote_quantity, fee)
            fifo_account.process_trade(trade)

# Print final positions, cash balance, and PnL
fifo_account.print_positions()
fifo_account.print_cash_balance()
fifo_account.print_pnl()

