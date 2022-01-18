#!/usr/bin/python
#filname: aws_find_user_iam_info.py
#description: boto example to get the user info from amazon iam
import boto3

iam = boto3.resource('iam')

all_info = boto3.resource('iam').CurrentUser().arn.split(':')
my_user= boto3.resource('iam').CurrentUser().arn.split(':')[5]

print ("all info from array is %s" % str(all_info) )
print ("my user is %s" % my_user)
