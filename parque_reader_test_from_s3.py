import pandas as pd
import s3fs
from datetime import datetime

def get_latest_slurm_date(bucket_prefix):
    """Extract the latest date from SLURM Parquet files in S3."""
    try:
        # Initialize S3 filesystem
        s3 = s3fs.S3FileSystem()

        # Find all parquet files
        files = s3.glob(f"{bucket_prefix}/slurm_*.parquet")
        if not files:
            raise Exception(f"No Parquet files found in {bucket_prefix}/")

        # Load and find max date
        latest_date = None
        for file in files:
            df = pd.read_parquet(file, filesystem=s3)
            if 'wake_time' in df.columns:
                current_max = pd.to_datetime(df['wake_time']).max()
                if latest_date is None or (current_max and current_max > latest_date):
                    latest_date = current_max

        if latest_date is None:
            raise Exception("No valid wake_time data found in Parquet files")

        return latest_date.to_pydatetime().date()

    except Exception as e:
        raise Exception(f"Error getting latest date: {str(e)}")

if __name__ == "__main__":
    # Simple Hello World test program
    BUCKET_PREFIX = "wqstm-data/tjk"
    try:
        latest_date = get_latest_slurm_date(BUCKET_PREFIX)
        print(f"Hello World! Latest SLURM date: {latest_date}")
    except Exception as e:
        print(f"Hello World! Error: {str(e)}")
