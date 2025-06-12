
# filename: calculate_aws_hpc_compute_cost.py
# usage: cat /var/log/slurmctld.log | python3 calculate_aws_hpc_compute_cost.py
#
# usage: calculate_aws_hpc_compute_cost.py [-h] [-C COST]
#
# Calculate compute batch durations and costs itemized by month.
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -C COST, --cost COST  Cost per hour per host (default: $1.591) based on
#                         7/8/24 prices

import sys
import re
import argparse
from datetime import datetime, timedelta

def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "[%Y-%m-%dT%H:%M:%S.%f]")

def parse_node_range(node_str):
    match = re.search(r'\[(\d+)-(\d+)\]', node_str)
    if match:
        start, end = map(int, match.groups())
        return end - start + 1
    return 1  # If no range is found, assume it's a single node

def calculate_cost(duration, hosts, cost_per_hour):
    hours = duration.total_seconds() / 3600
    return hours * hosts * cost_per_hour

def print_batch_info(batch_count, job_id, start_date, duration, hosts, cost):
    if cost > 0:
        print(f"Batch {batch_count}:")
        print(f"  Slurm Job ID: {job_id if job_id else 'Unknown'}")
        print(f"  Start date: {start_date.strftime('%Y-%m-%d')}")
        print(f"  Duration: {duration}")
        print(f"  Number of compute hosts: {hosts}")
        print(f"  Estimated cost: ${cost:.2f}")
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Calculate compute batch durations and costs itemized by month.")
    parser.add_argument("-C", "--cost", type=float, default=1.591,
                        help="Cost per hour per host (default: $1.591) based on 7/8/24 prices")
    args = parser.parse_args()

    suspend_time = None
    wake_time = None
    total_duration = timedelta(0)
    total_cost = 0
    batch_count = 0
    reported_batch_count = 0
    current_hosts = 0
    current_job_id = None

    # Dictionary to hold monthly costs
    monthly_costs = {}

    for line in sys.stdin:
        if "POWER: power_save: suspending nodes" in line:
            if wake_time:
                duration = parse_timestamp(line.split()[0]) - wake_time
                cost = calculate_cost(duration, current_hosts, args.cost)
                batch_count += 1

                if print_batch_info(batch_count, current_job_id, wake_time, duration, current_hosts, cost):
                    total_duration += duration
                    total_cost += cost
                    reported_batch_count += 1

                    # Get month-year key for monthly costs
                    month_year_key = wake_time.strftime("%Y-%m")
                    if month_year_key not in monthly_costs:
                        monthly_costs[month_year_key] = 0
                    monthly_costs[month_year_key] += cost

            suspend_time = parse_timestamp(line.split()[0])
            current_hosts = 0
            current_job_id = None

        elif "POWER: power_save: waking nodes" in line:
            wake_time = parse_timestamp(line.split()[0])
            node_str = line.split("waking nodes")[1].strip()
            current_hosts = parse_node_range(node_str)

        elif "Resetting JobId=" in line:
            job_id_match = re.search(r'JobId=(\d+)', line)
            if job_id_match:
                current_job_id = job_id_match.group(1)

    # Final calculation for the last batch if applicable
    if wake_time and suspend_time and wake_time < suspend_time:
        duration = suspend_time - wake_time
        cost = calculate_cost(duration, current_hosts, args.cost)
        batch_count += 1

        if print_batch_info(batch_count, current_job_id, wake_time, duration, current_hosts, cost):
            total_duration += duration
            total_cost += cost
            reported_batch_count += 1

            # Get month-year key for monthly costs
            month_year_key = wake_time.strftime("%Y-%m-%d")
            if month_year_key not in monthly_costs:
                monthly_costs[month_year_key] = 0
            monthly_costs[month_year_key] += cost

    # Output results including itemized monthly costs
    if reported_batch_count > 0:
        print(f"\nTotal batches (excluding $0 cost): {reported_batch_count}")
        print(f"Total compute time: {total_duration}")
        print(f"Total estimated cost: ${total_cost:.2f}")

        print("\nItemized Monthly Costs:")
        for month_year, cost in sorted(monthly_costs.items()):
            print(f"{month_year}: ${cost:.2f}")

    else:
        print("No compute batches with non-zero cost found in the log.")

if __name__ == "__main__":
    main()
