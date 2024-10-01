#filename: check_socket_all_interfaces.py
#description: gets the ip on all interfaces, and the hostname

import socket
import netifaces

def get_all_ip_addresses():
    ip_addresses = {}
    
    # Get the hostname
    hostname = socket.gethostname()
    ip_addresses['Hostname'] = hostname
    
    # Get all network interfaces
    interfaces = netifaces.interfaces()
    
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        
        # Get IPv4 addresses
        if netifaces.AF_INET in addrs:
            ipv4 = addrs[netifaces.AF_INET][0]['addr']
            ip_addresses[f'{interface} (IPv4)'] = ipv4
        
        # Get IPv6 addresses
        if netifaces.AF_INET6 in addrs:
            ipv6 = addrs[netifaces.AF_INET6][0]['addr']
            ip_addresses[f'{interface} (IPv6)'] = ipv6
    
    return ip_addresses

# Get and print all IP addresses
all_ips = get_all_ip_addresses()

print("Network Interface Information:")
for interface, ip in all_ips.items():
    print(f"{interface}: {ip}")

