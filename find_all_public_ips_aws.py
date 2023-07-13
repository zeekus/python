import logging
import os
import time
import boto3
import botocore

#these refer to the named profiles you use for aws cli and which are stored in C:\Users\<username>\.aws\credentials
profiles = [
    'default',
    'web',
    'hpc',
    'optimization'
]

regions = [
   'us-east-1',
   'us-east-2'
]

for profile in profiles:

  for region in regions:

    #set up session with appropriate profile and region, pull account id and account alias
    session = boto3.Session(profile_name=profile, region_name=region)
    acct_client = session.client('sts')
    acct_number = acct_client.get_caller_identity()["Account"]
    alias = session.client('iam').list_account_aliases()['AccountAliases'][0]

    #create ec2 client and set up pagination to pull enis
    ec2_client = session.client('ec2', region_name=region)
    paginator = ec2_client.get_paginator('describe_network_interfaces')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for network_interface in page['NetworkInterfaces']:
            public_ip = ''
            private_ip = ''
            instance_id = ''
            description = network_interface['Description']
            instance_owner_id = ''
            instance_name = ''
            #if Attachment exists then it is attached to something
            if 'Attachment' in network_interface:
              #if Association exists then it has a public IP
              if 'Association' in network_interface:
                public_ip = network_interface['Association']['PublicIp']
                #if InstanceId exists then we should pull other EC2 info
                if 'InstanceId' in network_interface['Attachment']:
                  instance_id = network_interface['Attachment']['InstanceId']
                  instance_owner_id = network_interface['Attachment']['InstanceOwnerId']
                  ec2_instance_tags = ec2_client.describe_tags(
                    Filters=[
                        {
                            'Name': 'resource-id',
                            'Values': [
                                instance_id
                            ],
                        },
                      ],
                    )
                  for tag in ec2_instance_tags["Tags"]:
                     if tag["Key"] == 'Name':
                        instance_name = tag["Value"]
                else:
                  #if not an Instance, InstanceOwnerId is the next best descriptor for what it is
                  instance_owner_id = network_interface['Attachment']['InstanceOwnerId']

                #package all set variables to a comma-delimited row
                row = "{},{},{},{},{},{},{},{}".format(acct_number, alias, region, public_ip, instance_id, instance_owner_id, instance_name, description)
                
                print(row)              
