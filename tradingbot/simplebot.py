import krakenex
import time
from pykrakenapi import KrakenAPI

# Initialize Kraken API
api = krakenex.API()
kraken = KrakenAPI(api)

# Set up trading parameters
pair = 'XXBTZUSD'  # Bitcoin-USD pair
check_interval = 1800  # 30 minutes in seconds
min_hold_time = 3600  # 1 hour in seconds

def get_volume_data():
    ohlc, last = kraken.get_ohlc_data(pair)
    return ohlc['volume']

def analyze_volume(current_volume, previous_volume):
    return current_volume > previous_volume * 1.1  # 10% increase threshold

def trading_strategy():
    last_trade_time = 0
    holding = False
    previous_volume = get_volume_data().iloc[-2]

    while True:
        current_time = time.time()
        current_volume = get_volume_data().iloc[-1]

        if holding:
            if current_time - last_trade_time >= min_hold_time:
                if not analyze_volume(current_volume, previous_volume):
                    # Sell when volume is slowing
                    print("Selling...")
                    # Implement sell order here
                    holding = False
        else:
            if analyze_volume(current_volume, previous_volume):
                # Buy when volume is increasing
                print("Buying...")
                # Implement buy order here
                holding = True
                last_trade_time = current_time

        previous_volume = current_volume
        time.sleep(check_interval)

if __name__ == "__main__":
    trading_strategy()
