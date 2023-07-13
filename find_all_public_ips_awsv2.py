import logging
import os
import time
import boto3
import botocore

# These refer to the named profiles you use for AWS CLI and which are stored in C:\Users\<username>\.aws\credentials
PROFILES = [
    'default',
#    'web',
#    'hpc',
#    'optimization'
]

REGIONS = [
    'us-east-1',
#    'us-east-2'
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_network_interfaces(profile, region):
    """Retrieve network interfaces for the specified profile and region."""
    session = boto3.Session(profile_name=profile, region_name=region)
    acct_client = session.client('sts')
    acct_number = acct_client.get_caller_identity()["Account"]
    alias = session.client('iam').list_account_aliases()['AccountAliases'][0]

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

            if 'Attachment' in network_interface:
                if 'Association' in network_interface:
                    public_ip = network_interface['Association']['PublicIp']
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
                        instance_owner_id = network_interface['Attachment']['InstanceOwnerId']

                    row = "{},{},{},{},{},{},{},{}".format(acct_number, alias, region, public_ip, instance_id, instance_owner_id, instance_name, description)
                    yield row

def main():
    """Main function to run the script."""
    for profile in PROFILES:
        for region in REGIONS:
            try:
                logging.info(f"Retrieving network interfaces for profile '{profile}' and region '{region}'...")
                for row in get_network_interfaces(profile, region):
                    print(row)
            except botocore.exceptions.ClientError as e:
                logging.error(f"Error retrieving network interfaces for profile '{profile}' and region '{region}': {e}")

if __name__ == '__main__':
    main()
