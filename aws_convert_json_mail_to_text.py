import json
import sys

#filename: aws_convert_json_mail_to_text.py
#description: convert an aws json  email into something readable by humans. 

# Function to convert JSON data to human-readable text
def json_to_readable(data):
    output = []

    output.append(f"Notification Type: {data.get('notificationType', 'N/A')}\n")

    # Bounce information
    bounce = data.get('bounce', {})
    output.append("Bounce Information:")
    output.append(f"  Feedback ID: {bounce.get('feedbackId', 'N/A')}")
    output.append(f"  Bounce Type: {bounce.get('bounceType', 'N/A')}")
    output.append(f"  Bounce Sub-Type: {bounce.get('bounceSubType', 'N/A')}")

    bounced_recipients = bounce.get('bouncedRecipients', [])
    if bounced_recipients:
        output.append("  Bounced Recipients:")
        for recipient in bounced_recipients:
            output.append(f"    - Email Address: {recipient.get('emailAddress', 'N/A')}")
            output.append(f"      Action: {recipient.get('action', 'N/A')}")
            output.append(f"      Status: {recipient.get('status', 'N/A')}")
            output.append(f"      Diagnostic Code: {recipient.get('diagnosticCode', 'N/A')}")

    output.append(f"  Timestamp: {bounce.get('timestamp', 'N/A')}")
    output.append(f"  Reporting MTA: {bounce.get('reportingMTA', 'N/A')}\n")

    # Mail information
    mail = data.get('mail', {})
    output.append("Mail Information:")
    output.append(f"  Timestamp: {mail.get('timestamp', 'N/A')}")
    output.append(f"  Source: {mail.get('source', 'N/A')}")
    output.append(f"  Source ARN: {mail.get('sourceArn', 'N/A')}")
    output.append(f"  Source IP: {mail.get('sourceIp', 'N/A')}")
    output.append(f"  Caller Identity: {mail.get('callerIdentity', 'N/A')}")
    output.append(f"  Sending Account ID: {mail.get('sendingAccountId', 'N/A')}")
    output.append(f"  Message ID: {mail.get('messageId', 'N/A')}")

    destination = mail.get('destination', [])
    if destination:
        output.append("  Destination:")
        for dest in destination:
            output.append(f"    - {dest}")

    headers = mail.get('headers', [])
    if headers:
        output.append("  Headers:")
        for header in headers:
            output.append(f"    - {header['name']}: {header['value']}")

    common_headers = mail.get('commonHeaders', {})
    if common_headers:
        output.append("  Common Headers:")
        for key, value in common_headers.items():
            if isinstance(value, list):
                value_str = ', '.join(value)
            else:
                value_str = value
            output.append(f"    - {key}: {value_str}")

    return "\n".join(output)

# Read JSON input from stdin
json_input = sys.stdin.read()

try:
    # Parse the JSON input
    data = json.loads(json_input)

    # Convert JSON to human-readable text
    readable_output = json_to_readable(data)

    # Print the human-readable text
    print(readable_output)

except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}", file=sys.stderr)
except KeyError as e:
    print(f"Error accessing key: {e}", file=sys.stderr)
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
