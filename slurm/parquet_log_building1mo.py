
#!/usr/bin/env python3
import sys
import re
import argparse
from datetime import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import s3fs

def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "[%Y-%m-%dT%H:%M:%S.%f]")

def parse_node_range(node_str):
    match = re.search(r'\[(\d+)-(\d+)\]', node_str)
    if match:
        start, end = map(int, match.groups())
        return end - start + 1
    return 1

def calculate_cost(duration, hosts, cost_per_hour):
    return (duration.total_seconds() / 3600) * hosts * cost_per_hour

def main():
    parser = argparse.ArgumentParser(description="Slurm Log Processor with S3 Parquet check/create")
    parser.add_argument("-C", "--cost", type=float, default=1.591)
    parser.add_argument("--s3-bucket", required=True, help="S3 bucket name (no trailing slash)")
    args = parser.parse_args()

    batches = []
    current_batch = {}

    # Process log lines
    for line in sys.stdin:
        line = line.strip()
        if "POWER: power_save: suspending nodes" in line:
            if current_batch.get('wake_time'):
                try:
                    current_batch['end_time'] = parse_timestamp(line.split()[0])
                    duration = current_batch['end_time'] - current_batch['wake_time']
                    current_batch['cost'] = calculate_cost(
                        duration,
                        current_batch['hosts'],
                        args.cost
                    )
                    current_batch['duration_seconds'] = int(duration.total_seconds())
                    batches.append(current_batch)
                except KeyError:
                    pass
                current_batch = {}

        elif "POWER: power_save: waking nodes" in line:
            current_batch['wake_time'] = parse_timestamp(line.split()[0])
            node_part = line.split("waking nodes")[1].strip()
            current_batch['hosts'] = parse_node_range(node_part)

        elif "Resetting JobId=" in line:
            job_match = re.search(r'JobId=(\d+)', line)
            if job_match:
                current_batch['job_id'] = job_match.group(1)

    if batches:
        # Create DataFrame with proper types
        df = pd.DataFrame(batches)
        df['wake_time'] = pd.to_datetime(df['wake_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])
        df['month_year'] = df['wake_time'].dt.strftime('%Y-%m')
        df['duration_seconds'] = df['duration_seconds'].astype('int64')
        df['hosts'] = df['hosts'].astype('int32')
        df['cost'] = df['cost'].round(2).astype('float32')

        # Initialize S3 filesystem
        s3 = s3fs.S3FileSystem()

        # Process each month's data
        for (month_year, monthly_data) in df.groupby('month_year'):
            s3_path = f"{args.s3_bucket}/slurm_{month_year}.parquet"
            print(f"Processing {s3_path}...")

            try:
                # Check if file exists
                if s3.exists(s3_path):
                    # Read existing data
                    try:
                        existing_df = pd.read_parquet(s3_path, filesystem=s3)
                    except Exception as e:
                        print(f"Error reading existing file {s3_path}: {e}")
                        existing_df = None
                else:
                    existing_df = None

                if existing_df is not None:
                    # Remove duplicates using job_id + wake_time
                    merge_cols = ['job_id', 'wake_time']
                    new_records_mask = ~monthly_data[merge_cols].apply(tuple, 1).isin(
                        existing_df[merge_cols].apply(tuple, 1)
                    )
                    monthly_data = monthly_data[new_records_mask]
                    combined_df = pd.concat([existing_df, monthly_data], ignore_index=True)
                else:
                    combined_df = monthly_data

                if not combined_df.empty:
                    combined_df.to_parquet(
                        s3_path,
                        filesystem=s3,
                        compression='SNAPPY',
                        index=False
                    )
                    print(f"Wrote {len(monthly_data)} new records, {len(combined_df)} total to {s3_path}")
                else:
                    print(f"No new records for {month_year}")

            except Exception as e:
                print(f"Error processing {month_year}: {str(e)}")

if __name__ == "__main__":
    main()
