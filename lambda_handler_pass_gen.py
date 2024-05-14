
#filename: lambda_handler_pass_gen.py
#description: an AWS lambda function to generate a random password with 10 characters of text with special characters and numbers.
#date: 5/14/24
#author: tjk

import random
import string
import boto3
from botocore.exceptions import ClientError


def generate_camel_case_string(length):
    # Generate a random string of lowercase letters
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))

    # Capitalize the first letter
    camel_case_string = random_string[0].upper() + random_string[1:]

    # Randomly capitalize some letters
    for i in range(1, len(camel_case_string)):
        if random.randint(0, 3) == 0:  # 25% chance of capitalizing a letter
            camel_case_string = camel_case_string[:i] + camel_case_string[i].upper() + camel_case_string[i+1:]

    return camel_case_string

def send_ses_mail(SENDER,RECIPIENT,SUBJECT,BODY_TEXT,region_name):
   
    # Create a new SES resource and specify a region.
    ses_client = boto3.client('ses', region_name)
    
    # Try to send the email.
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def lambda_handler(event, context):

    # Define email params
    # Set the email parameters
    SENDER = "myuser@example.com"
    RECIPIENT = SENDER
    SUBJECT = "Lambda called lambda_handler_pass_gen.py"
    BODY_TEXT = "Password updated in AWS Secrets. Please update things on your end."

    # Define character sets
    camelCase=generate_camel_case_string(length=10)
    digits = string.digits
    special_chars = "!@#$%^&*()_+{}|:<>?="

    # Generate 3 random base 10 numbers
    random_numbers = ''.join(random.choices(digits, k=3))

    # Generate random characters for the password
    password_chars = random.choices(camelCase + digits + special_chars, k=17)

    # Combine the random numbers and characters
    password = ''.join(random.sample(password_chars, len(password_chars)))
    password = random_numbers + password


    #send email about update
    send_ses_mail(SENDER,RECIPIENT,SUBJECT,BODY_TEXT,region_name="us-east-1")

    #print(password)

    return {
        'statusCode': 200,
        'body': password
    }

#lambda_handler("","")

