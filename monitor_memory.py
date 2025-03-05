#!/usr/bin/env python3

import os
import sys

def get_memory_usage():
    """Get memory usage percentage using /proc/meminfo"""
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.readlines()
        
        mem_total = None
        mem_available = None
        
        for line in meminfo:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1])
            elif line.startswith('MemAvailable:'):
                mem_available = int(line.split()[1])
            
            if mem_total is not None and mem_available is not None:
                break
        
        if mem_total and mem_available:
            # Calculate percentage of used memory
            mem_used_percent = 100 - (mem_available * 100 / mem_total)
            return mem_used_percent
        else:
            sys.stderr.write("Error: Could not parse memory information\n")
            sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error reading memory info: {str(e)}\n")
        sys.exit(1)

def check_memory_and_reboot(debug=False):
    # Get memory usage as a percentage
    memory_percent = get_memory_usage()
    
    if debug:
        print(f"Current memory usage: {memory_percent:.2f}%")
        print(f"Memory threshold: 95.00%")
        
        # Print more detailed memory info in debug mode
        try:
            print("Memory details:")
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    print(f"  {line.strip()}")
        except Exception as e:
            print(f"Error reading detailed memory info: {str(e)}")
            
        print(f"Would reboot if memory usage >= 95.00%")
    
    # Check if memory usage exceeds threshold
    if memory_percent >= 95.0:
        if debug:
            print("Memory threshold exceeded! Would execute reboot command.")
        else:
            print(f"Memory usage at {memory_percent:.2f}%, exceeding 95% threshold. Rebooting system.")
            os.system("sudo reboot")
    else:
        if debug:
            print("Memory usage is below threshold. No action needed.")

if __name__ == "__main__":
    # Check for debug flag
    debug_mode = True
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        debug_mode = True
    
    check_memory_and_reboot(debug_mode)

