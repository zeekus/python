import requests

API_STATUS_GRANTED = 'Granted'
API_STATUS_DENIED = 'Denied'

def log(msg):
    msg = 'Multifactor OpenVPN AS: {}'.format(msg)
    syslog.syslog(msg)

def get_country(ip_address):
    try:
        # Using ipapi to get geolocation information
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        # Return the country name
        return data.get("country_name")
    except requests.RequestException as e:
        print(f"Error retrieving location for IP {ip_address}: {e}")
        return None

def check_ip_and_disconnect(ip_address):
    country = get_country(ip_address)
    if country is None:
        print("Could not determine the country.")
        return
    
    print(f"IP Address: {ip_address} is from {country}.")
    
    if country != "United States":
        print("Disconnecting... User is not in the USA.")
        # Here you would implement your disconnect logic
    else:
        print("User is in the USA. Connection allowed.")

if __name__ == "__main__":
    try:
      # Make a request to ipify to get the public IP
      public_ip = requests.get('https://api.ipify.org').text
      print("Your Public IP Address is:", public_ip)
      check_ip_and_disconnect(public_ip)
    except requests.RequestException as e:
      print(f"Error retrieving public IP address: {e}")
      # Replace this with the actual IP address you want to check

