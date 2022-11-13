
import subprocess
proc=subprocess.run(['find','/home','-iname','GameLogs'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
directories=[] #may have more than one
directories=proc.stdout.rstrip().split("\n")  #remove white space at end of line and split by whitespace if more than one line
print(f"my dirs: '{directories}'")
for directory in directories:
    print(directory)
