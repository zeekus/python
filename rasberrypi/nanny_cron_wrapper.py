#filename: nanny_cron_wrapper.py
#description: run the nanny program from a cron job.

import os
import psutil
import subprocess

def check_and_start_process(process_name, command):
    # Check if the process is already running
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            print(f"Process '{process_name}' is already running.")
            return

    # Create a lock file to track the process state
    lock_file = f"{process_name}.lock"
    if os.path.isfile(lock_file):
        print(f"Process '{process_name}' is already running.")
        return
    else:
        # Start the process using nohup
        try:
            subprocess.Popen(["nohup"] + command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Started process '{process_name}' as nohup.")

            # Create the lock file
            with open(lock_file, 'w') as f:
                f.write("1")
        except Exception as e:
            print(f"Error starting process: {e}")

# Example usage:
check_and_start_process("night_time_nanny", "python night_time_nanny.py")
