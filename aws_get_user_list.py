#!/usr/bin/python3
#filename: aws_get_user_list.py
#description: gets list of aws users from IAM

import boto3
iam = boto3.client('iam')

paginator = iam.get_paginator('list_users')

for page in paginator.paginate():
  for user in page['Users']:
    print("User: {0}\nUserID: {1}\nARN: {2}\nCreatedOn: {3}\n".format( user['UserName'], user['UserId'], user['Arn'], user['CreateDate']))
