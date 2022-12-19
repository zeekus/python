#!/usr/bin/python3
#filename: restore-s3-objects.py
#description: moves files from Intelligent Tiering archive to Standard
#authors: Dave Kintgen and Theodore Knab

'''
  This script is used to restore objects from the AWS S3 service. It takes two arguments: the name of the S3 bucket and the path to the target folder within the bucket.

  Dependencies
  This script requires the following Python packages:
  - boto3
  - botocore

  Usage
  To use this script, run it from the command line with the following syntax:

  python3 restore-s3-objects.py [bucket name] [folder path]

  For example, to unfreeze all the files in the bbl directory inside the wqstm-data bucket, you would use the following command:
  python3 restore-s3-objects.py wqstm-data climate2019/cc31cm35/vtSFH/bbl/

  Example output: 
  command run: restore-s3-objects.py wqstm-data climate2019/cc31cm35/vtSFH/bbl/
  We are attempt to run.
  climate2019/cc31cm35/vtSFH/bbl/file1.txt
  file1.txt restored
  climate2019/cc31cm35/vtSFH/bbl/file2.txt
  file2.txt restored
  climate2019/cc31cm35/vtSFH/bbl/file3.txt
  file3.txt restored
  ...

  Error Handling
  If the script is called with the wrong number of arguments or if there is an issue restoring an object, an error message will be printed and the script will exit.

  - syntax error. You typed  ['restore-s3-objects.py']  We need some arguments. help function called.

  ['restore-s3-objects.py'] should have two values. The S3 bucket and the folder to target.
  For example, say you wanted to unfreeze all the files in the 'bbl' directory inside the wqstm-data bucket.
  use example:  restore-s3-objects.py wqstm-data climate2019/cc31cm35/vtSFH/bbl/
'''

import logging
import os
import time
import boto3
import botocore
import sys
#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

mybucket="mys3bucket"
myfolders="climate2019/run_cc31cm35/vtSFH/bbl/"

def helpme():
  print("help function called.\n")
  print(str(sys.argv), "should have two values. The S3 bucket and the folder to target.")
  print("For example, say you wanted to unfreeze all the files in the \'bbl\' directory inside the wqstm-data bucket.")
  print("use example: ", str(sys.argv[0]),  "mybucket climate2019/cc31cm35/vtSFH/bbl/" )

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
  page_iterator = paginator.paginate(Bucket=mybucket,Prefix=myfolders)

  for page in page_iterator:
    for object in page['Contents']:
      print(object['Key'])
      try:
        s3_client.restore_object(
          Bucket=mybucket,
          Key=object['Key'],
          RestoreRequest={
          'GlacierJobParameters': {
            'Tier': 'Standard'
          }
        })

        print('{object} restored'.format(object=object['Key']))
      except Exception as e:
        print('Key {object} not restorable'.format(object=object['Key']))
