class Trade:
    def __init__(self, date, base_asset, quote_asset, base_quantity, quote_quantity, fee):
        self.date = date
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.base_quantity = base_quantity
        self.quote_quantity = quote_quantity
        self.fee = fee
        self.price = abs(quote_quantity) / abs(base_quantity) if base_quantity != 0 else 0
        self.is_buy = (base_asset != 'USD' and base_quantity > 0) or (base_asset == 'USD' and quote_quantity < 0)

    def print_trade(self, line_number):
        action = "Buying" if self.is_buy else "Selling"
        if self.base_asset == 'USD':
            base_asset, quote_asset = self.quote_asset, self.base_asset
            base_quantity, quote_quantity = abs(self.quote_quantity), abs(self.base_quantity)
            price = 1 / self.price if self.price != 0 else 0
        else:
            base_asset, quote_asset = self.base_asset, self.quote_asset
            base_quantity, quote_quantity = abs(self.base_quantity), abs(self.quote_quantity)
            price = self.price
        
        print(f'{line_number}. Processing trade for {quote_asset}/{base_asset}')
        print(f'   Date: {self.date}')
        print(f'   Pair: {quote_asset}/{base_asset}')
        print(f'   Action: {action}')
        print(f'   {quote_asset}: {quote_quantity:.8f}')
        print(f'   {base_asset}: {base_quantity:.8f}')
        print(f'   Price: {price:.8f} {quote_asset}')
        print(f'   Fee: ${self.fee:.6f}')
        if self.is_buy:
            print(f'   Buying {base_quantity:.8f} {base_asset} at {price:.8f} {quote_asset} each for a total of {quote_quantity:.8f} {quote_asset}')
        else:
            print(f'   Selling {base_quantity:.8f} {base_asset} at {price:.8f} {quote_asset} each for a total of {quote_quantity:.8f} {quote_asset}')

def process_trade(self, trade):
    self.line_number += 1
    trade.print_trade(self.line_number)

    if trade.base_asset not in self.positions:
        self.positions[trade.base_asset] = deque()
    if trade.base_asset not in self.pnl:
        self.pnl[trade.base_asset] = 0

    if trade.is_buy:
        self.buy(trade)
    else:
        self.sell(trade)

