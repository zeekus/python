#!/usr/bin/python3
#filename: find_expiring_users.py
#description: use python to query get_secrets and get password from AWS secrets. Then query AD to find out what accounts are expiring.

# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import boto3
import base64
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "arn:aws:secretsmanager:us-east-1:6636233238198:secret:test-ldapadmin-XHB1"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            #print(secret)
            secret = secret.split(':')[1].replace("}"[-1],"").replace("\"","") #clean up string
            #print("final:'" + secret + "'")
            #for key,value in secret.items():
            # print(key, '->', value )
            # return (value)
            return secret #return password

        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            print(secret)


# Your code goes here.

# Math to convert MS time to Unix time
# AD's date format is 100 nanosecond intervals since Jan 1 1601 in GMT.
# To convert to seconds, divide by 10000000.
# To convert to UNIX, convert to positive seconds and subtract 1164473600 to be seconds since Jan 1 1970 (epoch).
def convert_time(ad_time):
  #  A value of 0 or 0x7FFFFFFFFFFFFFFF (9223372036854775807) indicates that the account never expires.
  # FIXME: Better handling of account-expires!
  if ad_time == "9223372036854775807":
     ad_time = "0"

  ad_seconds = (int(ad_time) / 10000000)
  #return ((int(ad_seconds) + 11644473600) if int(ad_seconds) != 0 else 0)
  return ((int(ad_seconds) - 11644473600) if int(ad_seconds) != 0 else 0)


mysecret=get_secret()

##############
#MAIN area
#query ldap using ldap3
##############


import re
import datetime
import ldap3
from ldap3 import Server, Connection, SAFE_SYNC, SUBTREE
server= Server('domaincontroller.example.net')

print("ldapserver",server)

user=('CN=LDAP Linux,OU=Service Accounts,OU=Non-Expiring Password Users,OU=Special Policies,DC=example,DC=net')
conn=Connection(server,user,mysecret, client_strategy=SAFE_SYNC, auto_bind=True)


# paged search wrapped in a generator
total_entries = 0

entry_generator = conn.extend.standard.paged_search(search_base = 'DC=example,DC=net',
                          search_filter = '(objectClass=user)',
                          search_scope = SUBTREE,
                          attributes = ['UserPrincipalName', 'Name', 'mail', 'msDS-UserPasswordExpiryTimeComputed' ],
                          paged_size = 5,
                          generator=False)


for entry in entry_generator:
    total_entries += 1
    #print(entry)
    #parsing dict
    for key,value in entry.items():
            if ( key == 'dn' ):
               if re.search(r'(?i)OU=Users', value) or re.search(r'(?i)OU=Administrators', value) :
                  print ("----------------------------------------")
                  dn=value
               else:
                  dn=''
            if ( key == 'attributes' and dn != '') :
              print("dn:", dn)
              print("name:",value['name'])
              print("key:",value['UserPrincipalName'])
              if ( len(value['mail']) > 2 ):
                 print("email:", value['mail'])
              else:
                 print("email: empty email for -> ",dn)
              mytime = value['msDS-UserPasswordExpiryTimeComputed']
              epoch_time=convert_time(mytime)
              print("expiration epoch:",epoch_time)
              print("expiration:",datetime.datetime.fromtimestamp(epoch_time))
              now_seconds=datetime.datetime.today().timestamp()
              days_remaining=( (epoch_time - now_seconds) / ( 60 * 60 * 24) )
              print("remaining:", days_remaining)



print('Total entries retrieved:', total_entries)



print (conn.search)
