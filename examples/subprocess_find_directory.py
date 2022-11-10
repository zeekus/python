
import subprocess
proc=subprocess.run(['find','/home','-iname','GameLogs'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
myfile= proc.stdout.strip()
print(f"my target file is '{myfile}'")