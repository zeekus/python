#!/usr/bin/python
#filename: aws_find_old_iam_keys.py
#description: boto example to determine if the current user has an old key
import boto3
from datetime import date
policy_days = 90 # 90 days

iam = boto3.resource('iam')
client = boto3.client('iam')

all_info = boto3.resource('iam').CurrentUser().arn.split(':')
my_user= boto3.resource('iam').CurrentUser().arn.split(':')[5]

print ("my user is %s" % my_user)
user=my_user.split('/')[1] #get user

res = client.list_access_keys(UserName=user)
accesskeydate = res['AccessKeyMetadata'][0]['CreateDate'].date()
currentdate = date.today()
active_days = currentdate - accesskeydate

if int(active_days.days) > policy_days:
  print ("Warning: The key for %s days old." % str(active_days.days))
else:
  print ("Ok: The key for %s days old." % str(active_days.days))
