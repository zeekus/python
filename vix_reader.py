"""
VIX Data List Reader
Lists all data stored in the parquet file with filtering and formatting options
"""

import pandas as pd
import sys
from pathlib import Path


def list_vix_data(parquet_file: str = 'vix_data.parquet', 
                  limit: int = None,
                  tail: int = None,
                  date_filter: str = None,
                  show_all_columns: bool = False):
    """
    List VIX data from parquet file
    
    Args:
        parquet_file: Path to parquet file
        limit: Show only first N rows (default: all)
        tail: Show only last N rows (default: None)
        date_filter: Filter by date (YYYY-MM-DD format)
        show_all_columns: Show all columns including calculated indicators
    """
    file_path = Path(parquet_file)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return
    
    # Load data
    df = pd.read_parquet(file_path)
    
    # Print summary
    print("="*80)
    print(f"VIX Data from: {file_path}")
    print("="*80)
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"VIX range: {df['vix'].min():.2f} to {df['vix'].max():.2f}")
    print(f"Columns: {', '.join(df.columns.tolist())}")
    print("="*80)
    print()
    
    # Filter by date if specified
    if date_filter:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        filter_date = pd.to_datetime(date_filter).date()
        df = df[df['date'] == filter_date]
        print(f"Filtered to date: {date_filter} ({len(df)} records)")
        df = df.drop('date', axis=1)
    
    # Select columns to display
    if show_all_columns:
        display_df = df
    else:
        # Show only main columns by default
        base_cols = ['timestamp', 'vix']
        optional_cols = ['rsi', 'macd_histogram', 'roc_5']
        display_cols = base_cols + [col for col in optional_cols if col in df.columns]
        display_df = df[display_cols]
    
    # Apply limit or tail
    if tail:
        display_df = display_df.tail(tail)
        print(f"Showing last {tail} records:")
    elif limit:
        display_df = display_df.head(limit)
        print(f"Showing first {limit} records:")
    else:
        print("Showing all records:")
    
    print()
    
    # Display data
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    print(display_df.to_string(index=True))
    
    print()
    print("="*80)


def export_to_csv(parquet_file: str = 'vix_data.parquet', 
                  output_file: str = 'vix_data.csv'):
    """
    Export parquet data to CSV for easier viewing
    
    Args:
        parquet_file: Input parquet file
        output_file: Output CSV file
    """
    file_path = Path(parquet_file)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return
    
    df = pd.read_parquet(file_path)
    df.to_csv(output_file, index=False)
    print(f"Exported {len(df)} records to: {output_file}")


def show_statistics(parquet_file: str = 'vix_data.parquet'):
    """
    Show detailed statistics about the VIX data
    
    Args:
        parquet_file: Path to parquet file
    """
    file_path = Path(parquet_file)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return
    
    df = pd.read_parquet(file_path)
    
    print("="*80)
    print("VIX DATA STATISTICS")
    print("="*80)
    
    # Basic info
    print(f"\nDataset Info:")
    print(f"  Total readings: {len(df)}")
    print(f"  Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"  Duration: {df['timestamp'].max() - df['timestamp'].min()}")
    
    # VIX statistics
    print(f"\nVIX Statistics:")
    print(f"  Current: {df['vix'].iloc[-1]:.2f}")
    print(f"  Mean: {df['vix'].mean():.2f}")
    print(f"  Median: {df['vix'].median():.2f}")
    print(f"  Std Dev: {df['vix'].std():.2f}")
    print(f"  Min: {df['vix'].min():.2f} (at {df.loc[df['vix'].idxmin(), 'timestamp']})")
    print(f"  Max: {df['vix'].max():.2f} (at {df.loc[df['vix'].idxmax(), 'timestamp']})")
    
    # RSI statistics if available
    if 'rsi' in df.columns:
        rsi_data = df['rsi'].dropna()
        if len(rsi_data) > 0:
            print(f"\nRSI Statistics:")
            print(f"  Current: {df['rsi'].iloc[-1]:.2f}")
            print(f"  Mean: {rsi_data.mean():.2f}")
            print(f"  Min: {rsi_data.min():.2f}")
            print(f"  Max: {rsi_data.max():.2f}")
            print(f"  Oversold (<30): {len(rsi_data[rsi_data < 30])} times")
            print(f"  Overbought (>70): {len(rsi_data[rsi_data > 70])} times")
    
    # Recent trend
    if len(df) >= 10:
        recent_change = df['vix'].iloc[-1] - df['vix'].iloc[-10]
        recent_pct = (recent_change / df['vix'].iloc[-10]) * 100
        print(f"\nRecent Trend (last 10 readings):")
        print(f"  Change: {recent_change:+.2f} ({recent_pct:+.2f}%)")
        print(f"  Direction: {'UP' if recent_change > 0 else 'DOWN' if recent_change < 0 else 'FLAT'}")
    
    print("="*80)


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("VIX Data List Reader")
        print("="*80)
        print("Usage:")
        print("  python vix_list_reader.py <command> [options]")
        print()
        print("Commands:")
        print("  list [file]              - List all data (default: vix_data.parquet)")
        print("  list [file] --limit N    - Show first N records")
        print("  list [file] --tail N     - Show last N records")
        print("  list [file] --date YYYY-MM-DD  - Filter by date")
        print("  list [file] --all        - Show all columns including indicators")
        print("  stats [file]             - Show statistics")
        print("  export [file] [output]   - Export to CSV")
        print()
        print("Examples:")
        print("  python vix_list_reader.py list")
        print("  python vix_list_reader.py list --tail 20")
        print("  python vix_list_reader.py list --date 2025-09-30")
        print("  python vix_list_reader.py list vix_data.parquet --all")
        print("  python vix_list_reader.py stats")
        print("  python vix_list_reader.py export vix_data.parquet output.csv")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        # Parse arguments
        parquet_file = 'vix_data.parquet'
        limit = None
        tail = None
        date_filter = None
        show_all = False
        
        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == '--limit' and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
                i += 2
            elif arg == '--tail' and i + 1 < len(sys.argv):
                tail = int(sys.argv[i + 1])
                i += 2
            elif arg == '--date' and i + 1 < len(sys.argv):
                date_filter = sys.argv[i + 1]
                i += 2
            elif arg == '--all':
                show_all = True
                i += 1
            elif not arg.startswith('--'):
                parquet_file = arg
                i += 1
            else:
                i += 1
        
        list_vix_data(parquet_file, limit=limit, tail=tail, 
                     date_filter=date_filter, show_all_columns=show_all)
    
    elif command == "stats":
        parquet_file = sys.argv[2] if len(sys.argv) > 2 else 'vix_data.parquet'
        show_statistics(parquet_file)
    
    elif command == "export":
        parquet_file = sys.argv[2] if len(sys.argv) > 2 else 'vix_data.parquet'
        output_file = sys.argv[3] if len(sys.argv) > 3 else 'vix_data.csv'
        export_to_csv(parquet_file, output_file)
    
    else:
        print(f"Unknown command: {command}")
        print("Use: list, stats, or export")
