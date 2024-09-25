import requests

try:
    # Make a request to ipify to get the public IP
    public_ip = requests.get('https://api.ipify.org').text
    print("Your Public IP Address is:", public_ip)
except requests.RequestException as e:
    print(f"Error retrieving public IP address: {e}")
