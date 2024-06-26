
#filename: lambda_handler_pass_gen.py
#description: an AWS lambda function to generate a random password with 10 characters of text with special characters and numbers.
#date: 5/14/24
#author: tjk

import random
import string
import boto3
from botocore.exceptions import ClientError
import datetime
import re

def is_us_holiday():
    # Get the current date
    today = datetime.date.today()
    
    # Check if today is Wednesday and not June 19th a new holiday. 
    if today.weekday() == 2:  # 0 = Monday, 1 = Tuesday, 2 = Wednesday, etc.
      # Check if today is not June 19th
      if not (today.month == 6 and today.day == 19):
        return ("Today is Wednesday and not June 19th")
      else:
        return ("Today is Wednesday, but it's also June 19th")
    else:
        return("Today is not Wednesday")



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

def send_ses_mail(SENDER, RECIPIENT, SUBJECT, BODY_TEXT, region_name):
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
        return response  # Return the response from send_email
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None  # Return None in case of an error

def lambda_handler(event, context):

    # Define email params
    # Set the email parameters
    SENDER = "myuser@myexample.com"
    RECIPIENT="myuser@myexample.com"
    SUBJECT =   "Lambda called lambda_handler_pass_gen.py"
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


    # Send email and get the response
    response = send_ses_mail(SENDER, RECIPIENT, SUBJECT, BODY_TEXT, region_name="us-east-1")

    if response and 'MessageId' in response:
        print("Email sent! Message ID:", response['MessageId'])
    else:
        print("Failed to send email.")
        
    pattern = r"Today is Wednesday and not June 19th"
    holiday_check=is_us_holiday()
    if re.search(pattern, holiday_check, re.IGNORECASE):
      #print(password)

      return {
        'statusCode': 200,
        'body': password
      }
    else:
      sys.exit(f"Error: {holiday_check}")

#lambda_handler("","")
