#!/usr/bin/python
#filename: aws_find_all_users_with_oldkeys.py
#description: boto example to list all the old keys from users
import boto3
from datetime import date
policy_days = 90 # 90 days

import boto3
iam_client = boto3.client('iam')
iam_resource = boto3.resource('iam')

paginator = iam_client.get_paginator('list_users')
badcount=0 #count of users over policy days
goodcount=0 #count of keys that are good
my_report=[]

for page in paginator.paginate():
  for user in page['Users']:
    if user['UserName'] != None :
      res = iam_client.list_access_keys(UserName=user['UserName'])#get client key info
      if res['AccessKeyMetadata'] != []: #some accounts have no keys. We ignore these.
        accesskeydate = res['AccessKeyMetadata'][0]['CreateDate'].date() #last change date
        currentdate = date.today() 
        active_days = currentdate - accesskeydate #math to find key age
        if int(active_days.days) > policy_days:
           my_report.append("User: {0}\nKeyID: {1}\nARN: {2}\nCreatedOn: {3}\nKeyAge: {4}\n".format( user['UserName'], user['UserId'], user['Arn'], user['CreateDate'], str(active_days.days) ))
           badcount = badcount + 1
        else:
          goodcount=goodcount+1

my_report.append("We found %3s users with keys older than %s days." % (badcount,policy_days) )
my_report.append("We found %3s users with keys less than %s days old." % (goodcount, policy_days) )
  
#display the report 
for line in my_report:
  print(line)