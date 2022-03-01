#!/usr/bin/python3
#description: check AWS keys and send an email if they are over the specifed limit days old.
#limitations: only works on Linux or BSD
#filename: aws_check_keys.py
#author: Theodore Knab

import re
import subprocess
import datetime
import boto3
import socket

limit=90 #90 day limit
emaildomain="example.net"
sent_from=(f"someone@{emaildomain}") #from _ddress
sent_to=(f"zeekus@{emaildomain}") #to _address
systemn=(socket.gethostname()) #system name

def get_aws_key():
  # get: aws iam list-access-keys
  process = subprocess.Popen(["aws","iam","list-access-keys"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout, stderr = process.communicate()
  stdout = stdout.decode('utf-8')
  if stderr is None:
   output=(stdout)
  else:
   stderr = stderr.decode('utf-8')
   output=(stderr)
  return output #return converted text

def find_how_many_days_past(limit,time_string):
  parsed_time=re.sub("\+.*","" ,time_string)
  date_time = datetime.datetime.strptime(parsed_time, "%Y-%m-%dT%H:%M:%S")
  a_timedelta = datetime.datetime.now() - date_time
  if datetime.timedelta(days=limit)< a_timedelta:
    expired=a_timedelta-datetime.timedelta(days=limit)
    print(f"aws key is old with an age of {a_timedelta}")
    print(f"key is {expired} overdue")
    return expired
  else:
    print("ok")
    return "ok"


def return_strings_cleanedup(regex_array,string_data):
  name=""
  myid=""
  status=""
  mydate=""
  for dataline in string_data.splitlines():
    for reline in regex_array:
     my_regex = re.escape(reline)
     p = re.compile(my_regex)

     if re.search(my_regex, dataline, re.IGNORECASE):
        if reline=="UserName":
           name=re.sub("[\"|,]", "", dataline.split(': ')[1])
        elif reline=="AccessKeyId":
           myid=re.sub("[\"|,]", "", dataline.split(': ')[1])
        elif reline=="Status":
           status=re.sub("[\"|,]", "", dataline.split(': ')[1])
        elif reline=="CreateDate":
           mydate=re.sub("[\"|,]", "", dataline.split(': ')[1])
        else:
           tmp=""

  return name,myid,status,mydate


def send_email(sent_from,sent_to,subject,body):
  # Replace sender@example.com with your "From" address.
  # This address must be verified with Amazon SES.
  #SENDER = "Sender Name <sender@example.com>"
  SENDER = ("Generic System <%s>" % sent_from)

  # Replace recipient@example.com with a "To" address. If your account
  # is still in the sandbox, this address must be verified.
  #RECIPIENT = "recipient@example.com"
  RECIPIENT = sent_to

  # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
  AWS_REGION = "us-east-1"

  # The subject line for the email.
  SUBJECT = subject
  BODY_TEXT=body

  # The character encoding for the email.
  CHARSET = "UTF-8"

  # Create a new SES resource and specify a region.
  client = boto3.client('ses',region_name=AWS_REGION)

  # Try to send the email.
  try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        #ConfigurationSetName=CONFIGURATION_SET,
    )
  # Display an error if something goes wrong.
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])


output=get_aws_key()
name,myid,status,mydate=return_strings_cleanedup(["UserName","AccessKeyId","Status","CreateDate"],output)

print(f"UserName: {name}")
print(f"AccessKeyId: {myid}")
print(f"Status: {status}")
print(f"CreateDate: {mydate}")
result=find_how_many_days_past(limit,time_string=mydate)

if result=="ok":
   print("ok, don't need to do anything")
   ok=1
else:
   print("send an email")
   send_email(sent_from,sent_to,subject=(f"Warning: {systemn} old aws key: {result} over limit"),body=(f"Your aws key on {systemn} may be {result} over the {limit} day policy limit."))
