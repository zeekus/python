# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/

import boto3                                #AWS 
import base64                               #AWS
import re                                   #for main
import subprocess                           #for main calling system 
from botocore.exceptions import ClientError #aws



def get_secret():

    secret_name = "prod-ldapadmin"
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
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            
    # Your code goes here. 

    print("secret1: " + secret)
    secret = re.sub(/^{|}$/,"",secret) #remove {} characters from outer edges if they exist
    print("secret2: " + secret)
    user_pass_list=secret.split(/":"/)
    user=user_pass_list.re.sub(/\"/,"",user_pass_list[0])
    pass=user_pass_list.re.sub(/\"/,"",user_pass_list[1])
    print ("debug - user: " + user)
    print ("debug - pass: " + pass)
    return pass

def reinit_kinit(pass,ldap_domain,ldap_user):
  print ("info: kdestroy run")
  proc = subprocess.Popen(['kdestroy','-A'], stdout=subprocess.PIPE)
  print("info: kinit run")
  print("debug - reinit_kinit function " + ldap_user)
  bind_user = (ldap_user + "@" + ldap_domain.upper())
  print ("debug - reinit_kinit function bind_user " + bind_user )
  proc = subprocess.Popen(['/bin/echo -n ',pass, " |/usr/bin/kinit ",bind_user], stdout=subprocess.PIPE)
  #clear cache in sssd. This fixes some group issues. 
  #ref https://jhrozek.wordpress.com/2016/12/09/restrict-the-set-of-groups-the-user-is-a-member-of-with-sssd/
  proc = subprocess.Popen(['/usr/sbin/sss_cache ','-E'], stdout=subprocess.PIPE)

############
#MAIN
############

#read in variables from a text file generated from YAML
filename=("/usr/local/admin/scripts/cron/ldap_variables.txt")
(secret_name,ldap_user,region_name,ldap_domain,ldap_ou,aws_access_key,aws_secret_key)=read_variables(filename)
  
status=""
#check klist as root
proc = subprocess.Popen(['/usr/bin/klist'], stdout=subprocess.PIPE)
text = proc.communicate()[0].decode('utf-8')

if re.search('Ticket cache: KEYRING:persistent', text, re.IGNORECASE):
   status=("ok")
  
if re.search('ok', status):
  print("Kerberos key ring assumed ok")
else:
  print ("please fix : kerberos refresh is needed")
  print ("secret_name is " + secret_name)
  print ("region_name is " + region_name)
  pass=get_secret(secret_name,region_name,aws_access_key,aws_secret_key) #get pass from secret manager
  reinit_kinit(pass,ldap_domain,ldap_user) #reinitualize with kinit