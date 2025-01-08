import click
import requests
import time
import pandas as pd
import numpy as np

@click.command()
@click.option('--starting-price', type=float, default=191.56, help='Starting price for the asset')
def run_bot(starting_price):
    # Set up trading parameters
    #pair = 'XMR/USD'  # Kraken uses this format for XMR/USD
    pair = 'SUI/USD'  # Kraken uses this format for SUI/USD
    check_interval = 60  # 15 minutes in seconds

    def get_ohlc_data(pair,interval=1):
      url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}"
      response = requests.get(url)
      data = response.json()
      if 'result' in data:
        ohlc = pd.DataFrame(data['result'][pair], 
                            columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')
        ohlc = ohlc.set_index('time')
        ohlc = ohlc.astype(float)
        
        # Calculate buy and sell volume
        ohlc['buy_volume'] = ohlc['volume'] * (ohlc['close'] > ohlc['open'])
        ohlc['sell_volume'] = ohlc['volume'] * (ohlc['close'] <= ohlc['open'])
        
        return ohlc
      else:
        click.echo(f"Error fetching data for {pair}: {data['error']}")
        return pd.DataFrame()


    # def get_ohlc_data(pair):
    #     url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval=15"
    #     response = requests.get(url)
    #     data = response.json()
    #     if 'result' in data:
    #         ohlc = pd.DataFrame(data['result'][pair], 
    #                             columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
    #         ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')
    #         ohlc = ohlc.set_index('time')
    #         ohlc = ohlc.astype(float)
    #         return ohlc
    #     else:
    #         click.echo(f"Error fetching data for {pair}: {data['error']}")
    #         return pd.DataFrame()

    def calculate_macd(data):
        close = data['close']
        exp1 = close.ewm(span=12, adjust=False).mean()
        exp2 = close.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal

    def trading_strategy(pair, starting_price):
        holdings = False
        buy_price = starting_price
        
        while True:
            ohlc_data = get_ohlc_data(pair)
            if ohlc_data.empty:
                continue
            
            current_price = float(ohlc_data['close'].iloc[-1])
            timestamp = ohlc_data.index[-1]

            # Analyze buy and sell volumes
            current_buy_volume = ohlc_data['buy_volume'].iloc[-1]
            current_sell_volume = ohlc_data['sell_volume'].iloc[-1]
            avg_buy_volume = ohlc_data['buy_volume'].iloc[-4:].mean()
            avg_sell_volume = ohlc_data['sell_volume'].iloc[-4:].mean()
        
            buy_volume_trend = "Increasing" if current_buy_volume > avg_buy_volume else "Decreasing"
            sell_volume_trend = "Increasing" if current_sell_volume > avg_sell_volume else "Decreasing"
        
            
            macd, signal = calculate_macd(ohlc_data)
            macd_value = macd.iloc[-1]
            signal_value = signal.iloc[-1]
            
            # Determine 15-minute trend based on MACD
            if macd_value > signal_value:
                trend = "Bullish"
            elif macd_value < signal_value:
                trend = "Bearish"
            else:
                trend = "Neutral"
            
            click.echo(f"Timestamp: {timestamp}")
            click.echo(f"Current price of {pair}: {current_price:.2f}")
            click.echo(f"1-minute MACD trend: {trend}")
            click.echo(f"MACD: {macd_value:.4f}, Signal: {signal_value:.4f}")
            click.echo(f"Current 1-minute buy volume: {current_buy_volume:.2f}")
            click.echo(f"Current 1-minute sell volume: {current_sell_volume:.2f}")
            click.echo(f"Buy volume trend: {buy_volume_trend} AVG: {avg_buy_volume}")
            click.echo(f"Sell volume trend: {sell_volume_trend} AVG: {avg_sell_volume}")
            
            if holdings:
                if current_price < buy_price * 0.95 or (trend == "Bearish" and current_price > buy_price * 1.05):
                    click.echo(f"Selling {pair} at {current_price:.2f}. Profit/Loss: {((current_price - buy_price) / buy_price * 100):.2f}%")
                    holdings = False
            else:
                if current_price < starting_price * 0.95 and trend == "Bullish":
                    click.echo(f"Buying {pair} at {current_price:.2f}")
                    holdings = True
                    buy_price = current_price
            
            click.echo("-------------------")
            time.sleep(check_interval)

    click.echo("Starting the trading bot...")
    trading_strategy(pair, starting_price)

if __name__ == "__main__":
    run_bot()

