class Trade:
    def __init__(self, date, crypto_asset, crypto_amount, usd_amount, fee, crypto_balance):
        self.date = date
        self.crypto_asset = crypto_asset
        self.crypto_amount = crypto_amount
        self.usd_amount = usd_amount
        self.fee = fee
        self.crypto_balance = crypto_balance
        self.is_buy = usd_amount < 0  # Buy if USD amount is negative
        self.actual_crypto_amount = crypto_amount - fee if self.is_buy else crypto_amount

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

