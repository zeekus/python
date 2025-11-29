import pandas as pd
#import time as time_module #for sleeps
from datetime import datetime,time
from pathlib import Path

#this should be run as a cron every 5mins

def is_market_open():
    """Check if US stock market is open"""
    now = datetime.now()

    # Weekend check
    if now.weekday() >= 5:  # 5=Saturday, 6=Sunday
        return False

    # Market hours: 7AM  - 8:00 PM UTC
    market_open = time(6, 55)
    market_close = time(20, 10)
    current_time = now.time()

    return market_open <= current_time <= market_close

def get_current_vix():
    """
    Fetch current VIX value from Yahoo Finance
    """
    import yfinance as yf
    
    try:
        vix = yf.Ticker("^VIX")
        data = vix.history(period="1d", interval="1m")
        
        if not data.empty:
            current_vix = data['Close'].iloc[-1]
            return round(current_vix, 2)
        else:
            print("No VIX data available")
            return None
            
    except Exception as e:
        print(f"Error fetching VIX: {e}")
        return None


class VIXRSILogger:
    def __init__(self, parquet_file='vix_data.parquet', rsi_period=14):
        """
        Initialize VIX logger with RSI calculation
        
        Args:
            parquet_file: Path to parquet file for storage
            rsi_period: Period for RSI calculation (default 14)
        """
        self.parquet_file = Path(parquet_file)
        self.rsi_period = rsi_period
        self.df = self._load_or_create_dataframe()
    
    def _load_or_create_dataframe(self):
        """Load existing parquet file or create new DataFrame"""
        if self.parquet_file.exists():
            print(f"Loading existing data from {self.parquet_file}")
            return pd.read_parquet(self.parquet_file)
        else:
            print("Creating new DataFrame to load data.")
            # Create empty DataFrame with proper dtypes
            return pd.DataFrame({
                'timestamp': pd.Series(dtype='datetime64[ns]'),
                'vix': pd.Series(dtype='float64'),
                'rsi': pd.Series(dtype='float64')
            })
    
    def calculate_rsi(self, df, period=14):
        """
        Calculate RSI (Relative Strength Index)
        
        Args:
            df: DataFrame with 'vix' column
            period: RSI period (default 14)
        
        Returns:
            Series with RSI values
        """
        # Calculate price changes
        delta = df['vix'].diff()
        
        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # Calculate average gain and loss using exponential moving average
        avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
        avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
        
        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def add_vix_reading(self, vix_value):
        """
        Add new VIX reading and recalculate RSI
        
        Args:
            vix_value: Current VIX value
        """
        # Create new row with proper dtypes
        new_row = pd.DataFrame({
            'timestamp': [pd.Timestamp(datetime.now())],
            'vix': [float(vix_value)],
            'rsi': [None]  # Will be calculated
        })
        
        # Use pd.concat with explicit ignore of empty check
        if len(self.df) == 0:
            self.df = new_row.copy()
        else:
            # Recalculate RSI for all data
            self.df = pd.concat([self.df, new_row], ignore_index=True)  # Subsequent rows - concat            
            #self.df['rsi'] = self.calculate_rsi(self.df, self.rsi_period)
        
        # Save to parquet
        self.df.to_parquet(self.parquet_file, index=False)
        
        # Print current status
        latest = self.df.iloc[-1]
        readings_needed = self.rsi_period + 1
        current_readings = len(self.df)
        
        if pd.notna(latest['rsi']):
            rsi_str = f"{latest['rsi']:.2f}"
        else:
            rsi_str = f"N/A (need {readings_needed - current_readings} more readings)"
        
        print(f"[{latest['timestamp']}] VIX: {latest['vix']:.2f} | RSI: {rsi_str} | Total readings: {current_readings}")
    
    def get_latest_rsi(self):
        """Get the most recent RSI value"""
        if len(self.df) > 0 and 'rsi' in self.df.columns:
            return self.df['rsi'].iloc[-1]
        return None
    
    def get_rsi_signal(self):
        """Get trading signal based on RSI"""
        rsi = self.get_latest_rsi()
        if rsi is None or pd.isna(rsi):
            return "INSUFFICIENT_DATA"
        elif rsi < 30:
            return "OVERSOLD"
        elif rsi > 70:
            return "OVERBOUGHT"
        else:
            return "NEUTRAL"
    
    def print_summary(self):
        """Print summary statistics"""
        if len(self.df) == 0:
            print("No data available")
            return
        
        print(f"\n{'='*60}")
        print(f"VIX RSI Summary")
        print(f"{'='*60}")
        print(f"Total readings: {len(self.df)}")
        print(f"Date range: {self.df['timestamp'].min()} to {self.df['timestamp'].max()}")
        print(f"\nCurrent VIX: {self.df['vix'].iloc[-1]:.2f}")
        
        if 'rsi' in self.df.columns and pd.notna(self.df['rsi'].iloc[-1]):
            print(f"Current RSI: {self.df['rsi'].iloc[-1]:.2f}")
            print(f"RSI Signal: {self.get_rsi_signal()}")
            print(f"\nRSI Statistics:")
            print(f"  Min: {self.df['rsi'].min():.2f}")
            print(f"  Max: {self.df['rsi'].max():.2f}")
            print(f"  Mean: {self.df['rsi'].mean():.2f}")
        else:
            print(f"RSI: Not enough data (need {self.rsi_period + 1}+ readings)")
        
        print(f"{'='*60}\n")
#end vix logger clas

def main():
    """Main execution function"""
    logger = VIXRSILogger(parquet_file='vix_data.parquet', rsi_period=14)

    print("Starting VIX RSI Logger...")
    print(f"Data will be saved to: {logger.parquet_file.absolute()}")  # Move here

    try:
        vix_value = get_current_vix()

        if vix_value is not None:
            logger.add_vix_reading(vix_value)

            # Print summary every 12 readings (1 hour if logging every 5 min)
            if len(logger.df) % 12 == 0:
                logger.print_summary()
            return 0
        else:
            print("Failed to fetch VIX data from Yahoo Finance")
            return 1

    except KeyboardInterrupt:
        print("\n\nStopping VIX RSI Logger...")
        logger.print_summary()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    if not is_market_open():
        print(f"Market closed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        with open('vix_logger_status.log', 'a') as f:
            f.write(f"{datetime.now()}: Market closed - skipping\n")
    else:
        exit_code = main()
        if exit_code == 1:
            print("VIX data fetch failed")
