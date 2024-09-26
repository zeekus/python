# OpenVPN Access Server IP post_auth script.
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
#
# Script last updated in January 2024

import re

from pyovpn.plugin import *


# If this is set to "NONE" or "DISABLED" then the server administrator must
# always manually register each IP address by hand on the command line.
# For that, we refer you to our documentation.
first_login_ip_addr = ""

# If False or undefined, AS will call us asynchronously in a worker thread.
# If True, AS will call us synchronously (server will block during call),
# however we can assume asynchronous behavior by returning a Twisted
# Deferred object.
SYNCHRONOUS=False

#########################
## IP Block Section
#########################

def post_auth(authcred, attributes, authret, info):
    print("********** POST_AUTH %s %s %s %s" % (authcred, attributes, authret, info))

    # get user's property list, or create it if absent
    proplist = authret.setdefault('proplist', {})

    # user properties to save - we will use this to pass the hw_addr_save property to be
    # saved in the user property database.
    proplist_save = {}

    error = ""

    # If a VPN client authentication attempt is made, do these steps:
    # Check if there is a known IP address for this client
    # If not, register it
    # If yes, check it
    #
    # An additional optional requirement is that first time registration must occur
    # from a specific IP address, as specified in the first_login_ip_addr set above
    #
    # The 'error' text goes to the VPN client and is shown to the user.
    # The 'print' lines go to the log file at /var/log/openvpnas.log (by default).

    if attributes.get('vpn_auth'):                   # Only do this for VPN authentication
        username = authcred.get('username')          # User name of the VPN client login attempt
        clientip = authcred.get('client_ip_addr')    # IP address of VPN client login attempt
        if clientip:
            clientip_save = proplist.get('pvt_clientip') # Saved IP address
            clientip_save2 = proplist.get('pvt_clientip2') # Saved IP address (secondary)
            if clientip_save:
                        if not clientip == clientip_save and not clientip == clientip_save2:
                            error = "The IP address reported by this VPN client does not match the registered IP address."
                            print("***** POST_AUTH IP CHECK: Account user name    : %s" % username)
                            print("***** POST_AUTH IP CHECK: Client IP address    : %s" % clientip)
                            if clientip_save2:
                                print("***** POST_AUTH IP CHECK: Client IP address    : %s or %s"  % (clientip_save, clientip_save2))
                            else:
                                print("***** POST_AUTH IP CHECK: Expected IP address  : %s" % clientip_save)
                            print("***** POST_AUTH IP CHECK: Connection attempt   : FAILED")
                        else:
                            print("***** POST_AUTH IP CHECK: Account user name    : %s" % username)
                            print("***** POST_AUTH IP CHECK: Client IP address    : %s" % clientip)
                            if clientip_save2:
                                print("***** POST_AUTH IP CHECK: Client IP address    : %s or %s"  % (clientip_save, clientip_save2))
                            else:
                                print("***** POST_AUTH IP CHECK: Expected IP address  : %s" % clientip_save)
                            print("***** POST_AUTH IP CHECK: Connection attempt   : SUCCESS")

            else:
                        # First login by this user, save IP addr.
                        if not first_login_ip_addr or first_login_ip_addr == clientip:
                            proplist_save['pvt_clientip'] = clientip
                            print("***** POST_AUTH IP CHECK: Account user name    : %s" % username)
                            print("***** POST_AUTH IP CHECK: Locked client IP     : %s" % clientip)
                            print("***** POST_AUTH IP CHECK: Action taken         : IP address learned and locked.")
                            print("***** POST_AUTH IP CHECK: Connection attempt   : SUCCESS")
                        else:
                            error = "Your attempt to login from a system not approved for IP address registration has been denied."
                            print("***** POST_AUTH IP CHECK: Account user name    : %s" % username)
                            print("***** POST_AUTH IP CHECK: Client IP address    : %s" % clientip)
                            print("***** POST_AUTH IP CHECK: Action taken         : attempt to register client IP address from unknown system denied.")
                            print("***** POST_AUTH IP CHECK: Connection attempt   : FAILED")

        else:
                error = "VPN client is not reporting an IP address. Please verify that a suitable OpenVPN client is being used."
                print("***** POST_AUTH IP CHECK: Account user name    : %s" % username)
                print("***** POST_AUTH IP CHECK: Client IP address    : NONE")
                print("***** POST_AUTH IP CHECK: IP address reported : %s" % clientip)
                print("***** POST_AUTH IP CHECK: Connection attempt   : FAILED")

    # process error, if one occurred
    if error:
        authret['status'] = FAIL
        authret['reason'] = error          # this error string is written to the server log file
        authret['client_reason'] = error   # this error string is reported to the client user

    return authret, proplist_save

