class FifoAccount:
    def __init__(self):
        self.positions = {}
        self.pnl = {}
        self.cash_balance = 0
        self.line_number = 0

    def process_trade(self, trade):
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

    def buy(self, trade):
        self.positions[trade.crypto_asset].append(trade)
        self.cash_balance -= abs(trade.usd_amount)

    def sell(self, trade):
        sell_quantity = abs(trade.crypto_amount)
        asset_queue = self.positions[trade.crypto_asset]
        self.cash_balance += abs(trade.usd_amount)

        total_profit = 0
        quantity_sold = 0

        while sell_quantity > 0 and asset_queue:
            oldest_trade = asset_queue[0]
            if oldest_trade.actual_crypto_amount <= sell_quantity:
                sell_quantity -= oldest_trade.actual_crypto_amount
                buy_price = abs(oldest_trade.usd_amount / oldest_trade.crypto_amount)
                sell_price = abs(trade.usd_amount / trade.crypto_amount)
                profit = (sell_price - buy_price) * oldest_trade.actual_crypto_amount
                total_profit += profit
                quantity_sold += oldest_trade.actual_crypto_amount
                print(f'   Sold {oldest_trade.actual_crypto_amount:.8f} {trade.crypto_asset} bought at {buy_price:.8f} USD. Profit: ${profit:.8f}')
                asset_queue.popleft()
            else:
                buy_price = abs(oldest_trade.usd_amount / oldest_trade.crypto_amount)
                sell_price = abs(trade.usd_amount / trade.crypto_amount)
                profit = (sell_price - buy_price) * sell_quantity
                total_profit += profit
                quantity_sold += sell_quantity
                print(f'   Sold {sell_quantity:.8f} {trade.crypto_asset} bought at {buy_price:.8f} USD. Profit: ${profit:.8f}')
                oldest_trade.actual_crypto_amount -= sell_quantity
                oldest_trade.usd_amount = oldest_trade.actual_crypto_amount * buy_price
                sell_quantity = 0

        if sell_quantity > 0:
            print(f"   Warning: Attempted to sell more {trade.crypto_asset} than available")

        self.pnl[trade.crypto_asset] += total_profit
        print(f'   Total profit for this sale: ${total_profit:.8f}')
        print(f'   Average sale price: ${abs(trade.usd_amount) / quantity_sold:.8f} USD per {trade.crypto_asset}')

    def print_positions(self):
        print("\nCurrent Positions:")
        for asset, queue in self.positions.items():
            total_quantity = sum(trade.actual_crypto_amount for trade in queue)
            if total_quantity > 0:
                print(f"{asset}: {total_quantity:.8f}")

    def print_cash_balance(self):
        print(f"\nCurrent Cash Balance: ${self.cash_balance:.4f}")

    def print_pnl(self):
        print("\nProfit/Loss per Asset:")
        for asset, profit in self.pnl.items():
            print(f"{asset}: ${profit:.8f}")
        print(f"Total PnL: ${sum(self.pnl.values()):.8f}")

