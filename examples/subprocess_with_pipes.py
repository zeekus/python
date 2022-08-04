import subprocess

# ps = subprocess.Popen(('ps', '-A'), stdout=subprocess.PIPE)
# output = subprocess.check_output(('grep', 'process_name'), stdin=ps.stdout)
# ps.wait()


echo  = subprocess.Popen(('echo', '-n','hello'), stdout=subprocess.PIPE)
output1 = subprocess.check_output(('grep', 'hell'), stdin=echo.stdout)
echo.wait()
print(output1)

error_code=subprocess.call("echo " + 'hello there' + "|" + 'grep -i hel', shell=True)
print(error_code)