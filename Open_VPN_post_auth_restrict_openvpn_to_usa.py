# OpenVPN Access Server US Only post_auth script.
#
# This script can be used with LOCAL, PAM, LDAP, RADIUS and SAML authentication.
# It adds an additional check when authentication is done through the VPN connection.
# It applies to all 3 connection profiles types (server-locked, user-locked, auto-login).
#
# This script will check the Source IP for a VPN Connection and allow/deny the VPN Attempt
# If the Source IP is configured to be allowed or denied
#
# Contributions by:
# Johan Draaisma
# Brandon Giron
# Theodore Knab
#
# Script last updated in January 2024


import requests
import syslog


# List of users who are exempt from location restrictions
exception_list = ['gbhatt@example.net', 'user2@example.net', 'user3@example.net']  # Override rules for SAML users

def log(msg):
    """Log messages to the syslog."""
    msg = 'OpenVPN AS: {}'.format(msg)
    syslog.syslog(msg)

def get_country(ip_address):
    """Retrieve the country name based on the provided IP address."""
    try:
        # Using ipapi to get geolocation information
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        # Return the country name
        return data.get("country_name")
    except requests.RequestException as e:
        log(f"Error retrieving location for IP {ip_address}: {e}")
        return None

def post_auth(authcred, attributes, authret, info):
    """Post-authentication checks for VPN access based on IP location."""
    print("********** POST_AUTH %s %s %s %s" % (authcred, attributes, authret, info))

    # Get user's property list or create it if absent
    proplist = authret.setdefault('proplist', {})

    # User properties to save - we will use this to pass the hw_addr_save property to be saved in the user property database.
    proplist_save = {}

    error = ""

    if attributes.get('vpn_auth'):  # Only do this for VPN authentication
        username = authcred.get('username')  # User name of the VPN client login attempt
        clientip = authcred.get('client_ip_addr')  # IP address of VPN client login attempt

        if clientip:  # Check if client IP is available
            if username not in exception_list:  # Check if user is not in the exception list
                country = get_country(clientip)  # Get the country based on IP address
                
                if country is None:
                    error = "Could not determine the country for the client IP address."
                    log(f"User: {username} at IP Address: {clientip}. Error: {error} ")
                elif country != "United States":
                    error = f"VPN access is restricted to users from the USA. Your country is {country}."
                    log(f"User: {username} at IP Address: {clientip}. Error: {error} ")
                else:
                    log(f"User: {username} at IP Address: {clientip} is from {country}. Connection allowed.")
            else:
                log(f"User: {username} is in the exception list. Connection allowed.")
        else:
            error = "VPN client is not reporting an IP address. Please verify that a suitable OpenVPN client is being used."
            log(f"User: {username} at IP Address: None. Error: {error}")

    # Process error, if one occurred
    if error:
        authret['status'] = FAIL  # Set status to FAIL
        authret['reason'] = error  # This error string is written to the server log file
        authret['client_reason'] = error  # This error string is reported to the client user

    return authret, proplist_save
