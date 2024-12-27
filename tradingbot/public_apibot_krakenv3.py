import click
import requests
import time
import pandas as pd
import numpy as np

@click.command()
@click.option('--starting-price', type=float, default=191.56, help='Starting price for the asset')
def run_bot(starting_price):
    pair = 'SUI/USD'  # Kraken uses this format for SUI/USD
    check_interval = 60  # Check every minute
    intervals = [1, 5, 30, 60, 240]  # 1m, 5m, 30m, 1h, 4h

    def get_ohlc_data(pair, interval):
        url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}"
        response = requests.get(url)
        data = response.json()
        if 'result' in data:
            ohlc = pd.DataFrame(data['result'][pair], 
                                columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
            ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')
            ohlc = ohlc.set_index('time')
            ohlc = ohlc.astype(float)
            
            ohlc['buy_volume'] = ohlc['volume'] * (ohlc['close'] > ohlc['open'])
            ohlc['sell_volume'] = ohlc['volume'] * (ohlc['close'] <= ohlc['open'])
            
            return ohlc
        else:
            click.echo(f"Error fetching data for {pair}: {data['error']}")
            return pd.DataFrame()

    def calculate_macd(data):
        close = data['close']
        exp1 = close.ewm(span=12, adjust=False).mean()
        exp2 = close.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal

    def analyze_data(ohlc_data, interval):
        if ohlc_data.empty:
            return

        current_price = float(ohlc_data['close'].iloc[-1])
        timestamp = ohlc_data.index[-1]

        current_buy_volume = ohlc_data['buy_volume'].iloc[-1]
        current_sell_volume = ohlc_data['sell_volume'].iloc[-1]
        avg_buy_volume = ohlc_data['buy_volume'].iloc[-4:].mean()
        avg_sell_volume = ohlc_data['sell_volume'].iloc[-4:].mean()

        buy_volume_trend = "Increasing" if current_buy_volume > avg_buy_volume else "Decreasing"
        sell_volume_trend = "Increasing" if current_sell_volume > avg_sell_volume else "Decreasing"

        macd, signal = calculate_macd(ohlc_data)
        macd_value = macd.iloc[-1]
        signal_value = signal.iloc[-1]

        trend = "Bullish" if macd_value > signal_value else "Bearish" if macd_value < signal_value else "Neutral"

        click.echo(f"{interval}-minute data:")
        click.echo(f"  Timestamp: {timestamp}")
        click.echo(f"  Current price: {current_price:.2f}")
        click.echo(f"  MACD trend: {trend}")
        click.echo(f"  MACD: {macd_value:.4f}, Signal: {signal_value:.4f}")
        click.echo(f"  Buy volume: {current_buy_volume:.2f} ({buy_volume_trend})")
        click.echo(f"  Sell volume: {current_sell_volume:.2f} ({sell_volume_trend})")
        click.echo("-------------------")

    def trading_strategy(pair, starting_price):
        holdings = False
        buy_price = starting_price
        
        while True:
            for interval in intervals:
                ohlc_data = get_ohlc_data(pair, interval)
                analyze_data(ohlc_data, interval)

            current_price = float(get_ohlc_data(pair, 1)['close'].iloc[-1])
            
            if holdings:
                if current_price < buy_price * 0.95:
                    click.echo(f"Selling {pair} at {current_price:.2f}. Profit/Loss: {((current_price - buy_price) / buy_price * 100):.2f}%")
                    holdings = False
            else:
                if current_price < starting_price * 0.95:
                    click.echo(f"Buying {pair} at {current_price:.2f}")
                    holdings = True
                    buy_price = current_price
            
            time.sleep(check_interval)

    click.echo("Starting the trading bot...")
    trading_strategy(pair, starting_price)

if __name__ == "__main__":
    run_bot()

