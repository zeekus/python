#!/usr/bin/python3
#filename: restore-s3-objects.py
#description: moves files from Intelligent Tiering archive to Standard
#authors: Dave Kintgen and Theodore Knab

import logging
import os
import time
import boto3
import botocore
import sys
#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

def helpme():
  print("help function called.\n")
  print(str(sys.argv), "should have two values. The S3 bucket and the folder to target.")
  print("For example, say you wanted to unfreeze all the files in the \'bbl\' directory inside the wqstm-data bucket.")
  print("use example: ", str(sys.argv[0]),  "wqstm-data climate2019/cc31cm35/vtSFH/bbl/" )

if len(sys.argv) <= 2 or len(sys.argv) > 3:
  if len(sys.argv) < 3:
    print("3 syntax error. You typed ", str(sys.argv), " We need some arguments.")
  elif len(sys.argv) > 3:
    print("syntax error. You typed ", str(sys.argv), " Too many arguments.")
  else :
    print("running")
  helpme()
  sys.exit()
else:
  print('command run:', str(sys.argv[0]),str(sys.argv[1]),str(sys.argv[2]))
  print ("We are attempt to run.")
  s3_client = boto3.client('s3')
  paginator = s3_client.get_paginator('list_objects_v2')
  page_iterator = paginator.paginate(Bucket='wqstm-data',Prefix='climate2019/run_cc31cm35/vtSFH/bbl/')

  for page in page_iterator:
    for object in page['Contents']:
      print(object['Key'])
      try:
        s3_client.restore_object(
          Bucket='wqstm-data',
          Key=object['Key'],
          RestoreRequest={
          'GlacierJobParameters': {
            'Tier': 'Standard'
          }
        })

        print('{object} restored'.format(object=object['Key']))
      except Exception as e:
        print('Key {object} not restorable'.format(object=object['Key']))
