def process_trade_pair(self, usd_trade, crypto_trade):
    """
    Handle a matched USD+crypto transaction from the same refid.
    We'll detect if it's a buy or sell by checking crypto_trade.is_buy.
    """
    self.line_number += 1
    print("----------------------------------------")
    print(f"{self.line_number:<3}")
    print('...Debug: process_trade_pair')
    print(f"...Processing trade pair for {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} linked by {usd_trade.refid}")

    if abs(crypto_trade.crypto_amount) < 1e-12:
        print(f"Warning: Zero crypto amount for {crypto_trade.crypto_asset}. Skipping.")
        return

    # price in USD per 1 unit of crypto
    price_each = abs(usd_trade.total_amt / crypto_trade.crypto_amount) if crypto_trade.crypto_amount != 0 else 0.0
    usd_fee_equiv = abs(crypto_trade.crypto_fee * price_each)

    # Update wallet balances for this specific asset pair
    wallet_key = f"{crypto_trade.crypto_asset}/USD"
    self.wallets[wallet_key] += usd_trade.crypto_amount

    # If it's a buy, we add net (crypto_amount - fee). If it's a sell, we add negative crypto_amount
    if crypto_trade.is_buy:
        self.wallets[wallet_key] += (crypto_trade.crypto_amount - crypto_trade.crypto_fee)
    else:
        self.wallets[wallet_key] += crypto_trade.crypto_amount

    # Protect from tiny negative rounding
    if self.wallets[wallet_key] < 0:
        self.wallets[wallet_key] = 0

    # Print the summary
    print(f" Date: {usd_trade.date}")
    print(f" Action: {'Buy' if crypto_trade.is_buy else 'Sell'}")
    print(f" {usd_trade.crypto_asset:<5}: {abs(usd_trade.crypto_amount):.8f}")
    print(f" {crypto_trade.crypto_asset:<5}: {abs(crypto_trade.crypto_amount):.8f}")
    print(f" Price for each {usd_trade.crypto_asset}/{crypto_trade.crypto_asset} pair: {price_each:.16f}")
    print(f" Total Amount {usd_trade.crypto_asset}: {abs(usd_trade.total_amt):.2f}")
    print(f" Crypto Fee: {crypto_trade.crypto_fee:.8f} {crypto_trade.crypto_asset}")
    print(f" USD Equivalent: {usd_fee_equiv:.9f}")
    print(f" Wallet balance for {wallet_key}: {self.wallets[wallet_key]:.8f}")

    # Distinguish buy vs sell
    if crypto_trade.is_buy:
        self._process_buy(usd_trade, crypto_trade)
    else:
        self._process_sell(usd_trade, crypto_trade)

    self.total_fees += usd_fee_equiv

