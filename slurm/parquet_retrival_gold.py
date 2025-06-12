# slurm_cost_report.py
import pandas as pd
import s3fs
from datetime import datetime, timedelta
from collections import defaultdict

folder="myfolder"
bucket="mybucket"


def generate_report(batch_data):
    """Generate formatted cost report from batch data"""
    total_batches = len(batch_data)
    total_cost = 0.0
    total_duration = timedelta()
    daily_stats = defaultdict(lambda: {'cost': 0.0, 'host_hours': 0.0, 'batches': 0})
    jobs = []

    # Process each batch
    for batch in batch_data:
        total_cost += batch['cost']
        total_duration += batch['duration']

        # Aggregate daily stats
        date_key = batch['start_date'].strftime('%Y-%m-%d')
        daily_stats[date_key]['cost'] += batch['cost']
        daily_stats[date_key]['host_hours'] += batch['hosts'] * (batch['duration'].total_seconds()/3600)
        daily_stats[date_key]['batches'] += 1
        jobs.append(batch)

    # Build report sections
    report = []
    report.append("=== SLURM COMPUTE COST REPORT ===")
    report.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Summary section
    report.append("--- Summary ---")
    report.append(f"Total Batches: {total_batches}")
    report.append(f"Total Compute Hours: {total_duration.total_seconds()/3600:.1f}h")
    report.append(f"Total Estimated Cost: ${total_cost:.2f}\n")

    # Daily breakdown
    report.append("--- Daily Breakdown ---")
    for date in sorted(daily_stats.keys()):
        stats = daily_stats[date]
        report.append(f"{date}: {stats['batches']} batches | Cost: ${stats['cost']:.2f} | Host-Hours: {stats['host_hours']:.1f}h")

    # Top costly jobs
    report.append("\n--- Top Costly Jobs ---")
    sorted_jobs = sorted(jobs, key=lambda x: x['cost'], reverse=True)[:5]
    for idx, job in enumerate(sorted_jobs, 1):
        duration_str = str(job['duration']).split('.')[0]  # Remove microseconds
        report.append(
            f"{idx}. [Job {job['job_id']}] {job['start_date'].strftime('%Y-%m-%d')} | "
            f"{duration_str} | "
            f"{job['hosts']} hosts | "
            f"${job['cost']:.2f}"
        )

    # Cost efficiency
    total_host_hours = sum(stats['host_hours'] for stats in daily_stats.values())
    if total_host_hours > 0:
        cost_per_host_hour = total_cost / total_host_hours
        report.append(f"\nCost Efficiency: ${cost_per_host_hour:.3f}/host-hour")

    return '\n'.join(report)

def load_s3_data(bucket_prefix):
    """Load and process data from S3 Parquet files"""
    s3 = s3fs.S3FileSystem()
    # Find all parquet files in the directory
    files = s3.glob(f"{bucket_prefix}/slurm_*.parquet")
    if not files:
        raise Exception(f"No Parquet files found in {bucket_prefix}/")
    dfs = []
    for file in files:
        df = pd.read_parquet(file, filesystem=s3)
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    # Figure out which duration column is present
    if 'duration_seconds' in df.columns:
        get_duration = lambda row: timedelta(seconds=int(row['duration_seconds']))
    elif 'duration' in df.columns:
        # If duration is already a timedelta, just use it
        get_duration = lambda row: row['duration'] if isinstance(row['duration'], timedelta) else timedelta(seconds=int(row['duration']))
    else:
        raise Exception("No duration column found in Parquet files.")
    # Build batch records
    batches = []
    for _, row in df.iterrows():
        batches.append({
            'job_id': str(row['job_id']),
            'start_date': pd.to_datetime(row['wake_time']).to_pydatetime(),
            'duration': get_duration(row),
            'hosts': int(row['hosts']),
            'cost': float(row['cost'])
        })
    return batches

if __name__ == "__main__":
    BUCKET_PREFIX = "{bucket}/{folder}"
    try:
        batch_data = load_s3_data(BUCKET_PREFIX)
        report = generate_report(batch_data)
        print(report)
    except Exception as e:
        print(f"Error generating report: {str(e)}")
