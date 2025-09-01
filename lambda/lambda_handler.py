import json
import boto3
import os

# Initialize AWS clients
sns = boto3.client('sns')
logger = boto3.client('logs')

# Get environment variables
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    try:
        # Iterate through CloudTrail events
        for record in event['Records']:
            log_data = json.loads(record['Sns']['Message'])
            
            # Extract key details from CloudTrail event
            event_name = log_data.get('eventName', 'UnknownEvent')
            user_identity = log_data.get('userIdentity', {})
            source_ip = log_data.get('sourceIPAddress', 'UnknownIP')
            timestamp = log_data.get('eventTime', 'UnknownTime')

            # Print log for debugging
            print(f"CloudTrail Event: {log_data}")
            
            # Check for specific events (e.g., UnauthorizedOperation)
            if event_name == "UnauthorizedOperation":
                # Construct alert message
                alert_message = (
                    f"ALERT: UnauthorizedOperation detected!\n\n"
                    f"User: {user_identity.get('arn', 'UnknownUser')}\n"
                    f"Source IP: {source_ip}\n"
                    f"Event Time: {timestamp}\n"
                    f"Event Details: {json.dumps(log_data, indent=4)}"
                )
                print(alert_message)
                
                # Send notification via SNS
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=alert_message,
                    Subject="CloudTrail UnauthorizedOperation Alert"
                )

    except Exception as e:
        print(f"Error processing event: {str(e)}")
        raise

