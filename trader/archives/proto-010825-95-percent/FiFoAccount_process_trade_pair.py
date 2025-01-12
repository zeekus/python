def process_trade_pair(self, usd_trade, crypto_trade):
    self.line_number += 1
    cost_basis = abs(usd_trade.total_amt / crypto_trade.crypto_amount)
    usd_fee_equivalent = abs(crypto_trade.crypto_fee * cost_basis)
    
    print(f"----------------------------------------")
    print(f"{self.line_number:<3}")
    print(f"...Processing trade pair for {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} linked by {usd_trade.refid}")
    print(f"   Date: {usd_trade.date}")
    print(f"   Action: Pairing transaction")
    print(f"   {usd_trade.crypto_asset:<5}: {abs(usd_trade.crypto_amount):<10.8f}")
    print(f"   {crypto_trade.crypto_asset:<5}: {crypto_trade.crypto_amount:<10.8f}")
    print(f"   Cost Basis for each {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} pair: {cost_basis:.16f}")
    print(f"   Total Amount {usd_trade.crypto_asset}: {abs(usd_trade.total_amt):<10.2f}")
    print(f"   Crypto Fee: {crypto_trade.crypto_fee:<10.8f} {crypto_trade.crypto_asset}")
    print(f"   USD Equivalent: {usd_fee_equivalent:<10.9f}")
    
    self.wallets[usd_trade.crypto_asset] += usd_trade.crypto_amount
    self.wallets[crypto_trade.crypto_asset] += crypto_trade.crypto_amount
    
    # Check and reset wallet balances if they go negative
    for asset in [usd_trade.crypto_asset, crypto_trade.crypto_asset]:
        if self.wallets[asset] < 0:
            self.wallets[asset] = 0
    
    print(f"   {usd_trade.crypto_asset:<5} Wallet balance: {self.wallets[usd_trade.crypto_asset]:<10.8f}")
    print(f"   {crypto_trade.crypto_asset:<5} Wallet balance: {self.wallets[crypto_trade.crypto_asset]:<10.8f}")

    if crypto_trade.is_buy:
        self.positions[crypto_trade.crypto_asset].append((crypto_trade.actual_crypto_amount, cost_basis))
        self.cash_balance -= abs(usd_trade.total_amt)
    else:
        self.sell(crypto_trade, abs(usd_trade.total_amt))
        self.cash_balance += abs(usd_trade.total_amt)

    # Check and reset cash balance if it goes negative
    if self.cash_balance < 0:
        self.cash_balance = 0

    self.total_fees += crypto_trade.crypto_fee * cost_basis
