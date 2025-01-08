import pandas as pd
from collections import deque

class Trade:
    def __init__(self, date, crypto_asset, crypto_amount, usd_amount, fee, crypto_balance):
        self.date = date
        self.crypto_asset = crypto_asset
        self.crypto_amount = crypto_amount
        self.usd_amount = usd_amount
        self.fee = fee
        self.crypto_balance = crypto_balance
        self.is_buy = usd_amount < 0  # Buy if USD amount is negative

    def print_trade(self, line_number):
        action = "Buying" if self.is_buy else "Selling"
        price = abs(self.usd_amount / self.crypto_amount)
        print(f'{line_number}. Processing trade for {self.crypto_asset}/USD')
        print(f'   Date: {self.date}')
        print(f'   Action: {action}')
        print(f'   {self.crypto_asset}: {abs(self.crypto_amount):.8f}')
        print(f'   USD: {abs(self.usd_amount):.8f}')
        print(f'   Price: {price:.8f} USD per {self.crypto_asset}')
        print(f'   Fee: ${self.fee:.6f}')
        print(f'   {self.crypto_asset} Balance: {self.crypto_balance:.8f}')
        if self.is_buy:
            print(f'   Buying {abs(self.crypto_amount):.8f} {self.crypto_asset} at {price:.8f} USD each for a total of {abs(self.usd_amount):.8f} USD')
        else:
            print(f'   Selling {abs(self.crypto_amount):.8f} {self.crypto_asset} at {price:.8f} USD each for a total of {abs(self.usd_amount):.8f} USD')

class FifoAccount:
    def __init__(self):
        self.positions = {}
        self.pnl = {}
        self.cash_balance = 0
        self.line_number = 0

    def process_trade(self, trade):
        
        if self.line_number == 0:
          self.cash_balance = abs(trade.usd_amount)  # Initialize cash balance with first trade
        self.line_number += 1
        trade.print_trade(self.line_number)

        if trade.crypto_asset not in self.positions:
            self.positions[trade.crypto_asset] = deque()
        if trade.crypto_asset not in self.pnl:
            self.pnl[trade.crypto_asset] = 0

        if trade.is_buy:
            self.buy(trade)
        else:
            self.sell(trade)

    # def buy(self, trade):
    #     self.positions[trade.crypto_asset].append(trade)
    #     self.cash_balance += trade.usd_amount  # Decrease cash balance (usd_amount is negative for buys)
    def buy(self, trade):
      self.positions[trade.crypto_asset].append(trade)
      self.cash_balance -= abs(trade.usd_amount)  # Decrease cash balance by the absolute value of USD amount



    def sell(self, trade):
     sell_quantity = abs(trade.crypto_amount)
     asset_queue = self.positions[trade.crypto_asset]
     #self.cash_balance += trade.usd_amount  # Increase cash balance
     self.cash_balance += abs(trade.usd_amount)  # Increase cash balance by the absolute value of USD amount

     total_profit = 0
     quantity_sold = 0

     while sell_quantity > 0 and asset_queue:
        oldest_trade = asset_queue[0]
        if oldest_trade.crypto_amount <= sell_quantity:
            sell_quantity -= oldest_trade.crypto_amount
            buy_price = abs(oldest_trade.usd_amount / oldest_trade.crypto_amount)
            sell_price = abs(trade.usd_amount / trade.crypto_amount)
            profit = (sell_price - buy_price) * oldest_trade.crypto_amount
            total_profit += profit
            quantity_sold += oldest_trade.crypto_amount
            print(f'   Sold {oldest_trade.crypto_amount:.8f} {trade.crypto_asset} bought at {buy_price:.8f} USD. Profit: ${profit:.8f}')
            asset_queue.popleft()
        else:
            buy_price = abs(oldest_trade.usd_amount / oldest_trade.crypto_amount)
            sell_price = abs(trade.usd_amount / trade.crypto_amount)
            profit = (sell_price - buy_price) * sell_quantity
            total_profit += profit
            quantity_sold += sell_quantity
            print(f'   Sold {sell_quantity:.8f} {trade.crypto_asset} bought at {buy_price:.8f} USD. Profit: ${profit:.8f}')
            oldest_trade.crypto_amount -= sell_quantity
            oldest_trade.usd_amount = oldest_trade.crypto_amount * buy_price  # Update the USD amount for the remaining crypto
            sell_quantity = 0

     if sell_quantity > 0:
        print(f"   Warning: Attempted to sell more {trade.crypto_asset} than available")

     self.pnl[trade.crypto_asset] += total_profit
     print(f'   Total profit for this sale: ${total_profit:.8f}')
     print(f'   Average sale price: ${abs(trade.usd_amount) / quantity_sold:.8f} USD per {trade.crypto_asset}')


    # def sell(self, trade):
    #     sell_quantity = abs(trade.crypto_amount)
    #     asset_queue = self.positions[trade.crypto_asset]
    #     self.cash_balance += trade.usd_amount  # Increase cash balance

    #     total_profit = 0
    #     quantity_sold = 0

    #     while sell_quantity > 0 and asset_queue:
    #         oldest_trade = asset_queue[0]
    #         if oldest_trade.crypto_amount <= sell_quantity:
    #             sell_quantity -= oldest_trade.crypto_amount
    #             buy_price = abs(oldest_trade.usd_amount / oldest_trade.crypto_amount)
    #             sell_price = abs(trade.usd_amount / trade.crypto_amount)
    #             profit = (sell_price - buy_price) * oldest_trade.crypto_amount
    #             total_profit += profit
    #             quantity_sold += oldest_trade.crypto_amount
    #             print(f'   Sold {oldest_trade.crypto_amount:.8f} {trade.crypto_asset} bought at {buy_price:.8f} USD. Profit: ${profit:.8f}')
    #             asset_queue.popleft()
    #         else:
    #             buy_price = abs(oldest_trade.usd_amount / oldest_trade.crypto_amount)
    #             sell_price = abs(trade.usd_amount / trade.crypto_amount)
    #             profit = (sell_price - buy_price) * sell_quantity
    #             total_profit += profit
    #             quantity_sold += sell_quantity
    #             print(f'   Sold {sell_quantity:.8f} {trade.crypto_asset} bought at {buy_price:.8f} USD. Profit: ${profit:.8f}')
    #             oldest_trade.crypto_amount -= sell_quantity
    #             oldest_trade.usd_amount -= sell_quantity * buy_price  # Update the USD amount for the remaining crypto
    #             sell_quantity = 0

    #     if sell_quantity > 0:
    #         print(f"   Warning: Attempted to sell more {trade.crypto_asset} than available")

    #     self.pnl[trade.crypto_asset] += total_profit
    #     print(f'   Total profit for this sale: ${total_profit:.8f}')
    #     print(f'   Average sale price: ${abs(trade.usd_amount) / quantity_sold:.8f} USD per {trade.crypto_asset}')

    def print_positions(self):
        print("\nCurrent Positions:")
        for asset, queue in self.positions.items():
            total_quantity = sum(trade.crypto_amount for trade in queue)
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

        if row1['type'] == 'trade' and row2['type'] == 'trade':
            date = pd.to_datetime(row1['time'])
            
            if row1['asset'] == 'USD':
                usd_row = row1
                crypto_row = row2
            else:
                usd_row = row2
                crypto_row = row1

            crypto_asset = crypto_row['asset']
            crypto_amount = float(crypto_row['amount'])
            usd_amount = float(usd_row['amount'])
            fee = float(crypto_row['fee'])
            crypto_balance = float(crypto_row['balance'])

            trade = Trade(date, crypto_asset, crypto_amount, usd_amount, fee, crypto_balance)
            fifo_account.process_trade(trade)

# Print final positions, cash balance, and PnL
fifo_account.print_positions()
fifo_account.print_cash_balance()
fifo_account.print_pnl()

