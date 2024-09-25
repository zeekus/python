import socket

# Get the hostname of the current machine
hostname = socket.gethostname()

# Get the local IP address using the hostname
local_ip = socket.gethostbyname(hostname)

print("Your Computer Name is:", hostname)
print("Your Local IP Address is:", local_ip)
