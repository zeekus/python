import click
import requests
import time
import pandas as pd
import numpy as np

@click.command()
@click.option('--starting-price', type=float, default=191.56, help='Starting price for the asset')
def run_bot(starting_price):
    # Set up trading parameters
    pair = 'XMR/USD'
    check_interval = 300  # 5 minutes in seconds

    def get_ohlc_data(pair):
        url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval=60"
        response = requests.get(url)
        data = response.json()
        if 'result' in data:
            ohlc = pd.DataFrame(data['result'][pair], 
                                columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
            ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')
            ohlc = ohlc.set_index('time')
            ohlc = ohlc.astype(float)
            return ohlc
        else:
            click.echo(f"Error fetching data for {pair}: {data['error']}")
            return pd.DataFrame()

    def get_current_price(pair):
        url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
        response = requests.get(url)
        data = response.json()
        if 'result' in data:
            return float(data['result'][pair]['c'][0])  # Current price
        else:
            click.echo(f"Error fetching current price for {pair}: {data['error']}")
            return None

    def trading_strategy(pair, starting_price):
        holdings = False
        buy_price = starting_price
        
        while True:
            current_price = get_current_price(pair)
            print (f"current price is {current_price}")
            if current_price is None:
                continue
            
            if holdings:
                if current_price < buy_price * 0.95:  # 5% stop loss
                    click.echo(f"Selling {pair} at {current_price:.2f}. Loss: {((current_price - buy_price) / buy_price * 100):.2f}%")
                    holdings = False
                elif current_price > buy_price * 1.1:  # 10% profit target
                    click.echo(f"Selling {pair} at {current_price:.2f}. Profit: {((current_price - buy_price) / buy_price * 100):.2f}%")
                    holdings = False
            else:
                if current_price < starting_price * 0.95:  # Buy if price drops 5% below starting price
                    click.echo(f"Buying {pair} at {current_price:.2f}")
                    holdings = True
                    buy_price = current_price
            
            time.sleep(check_interval)

    click.echo("Starting the trading bot...")
    trading_strategy(pair, starting_price)

if __name__ == "__main__":
    run_bot()
