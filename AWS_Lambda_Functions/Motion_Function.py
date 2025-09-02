import json
import boto3
import os
from decimal import Decimal
import time

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
cloudwatch = boto3.client('cloudwatch') 

DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'MotionData')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:867344433481:AbnormalMotionAlert')
MOTION_THRESHOLD = 1.8

def lambda_handler(event, context):
    try:
        # Directly parse IoT payload
        payload = json.loads(json.dumps(event), parse_float=Decimal)
        
        # Extract data from payload
        acceleration_x = payload.get('acceleration_x', 0)
        acceleration_y = payload.get('acceleration_y', 0)
        acceleration_z = payload.get('acceleration_z', 0)
        
        # Handle missing or invalid timestamp
        timestamp = payload.get('timestamp')
        if not timestamp:
            timestamp = int(time.time())  
        
        # Ensure timestamp is a valid number
        try:
            timestamp = int(timestamp)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid timestamp value: {timestamp}")

        device_id = payload.get('device_id', 'Motion_Thing')

        # Store data in DynamoDB
        table = dynamodb.Table(DYNAMODB_TABLE)
        table.put_item(Item={
            'deviceId': device_id,
            'timestamp': timestamp,
            'acceleration_x': acceleration_x,
            'acceleration_y': acceleration_y,
            'acceleration_z': acceleration_z
        })

        # Send acceleration metrics to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='MotionData',
            MetricData=[
                {
                    'MetricName': 'AccelerationX',
                    'Dimensions': [{'Name': 'DeviceID', 'Value': device_id}],
                    'Value': acceleration_x,
                    'Unit': 'None'
                },
                {
                    'MetricName': 'AccelerationY',
                    'Dimensions': [{'Name': 'DeviceID', 'Value': device_id}],
                    'Value': acceleration_y,
                    'Unit': 'None'
                },
                {
                    'MetricName': 'AccelerationZ',
                    'Dimensions': [{'Name': 'DeviceID', 'Value': device_id}],
                    'Value': acceleration_z,
                    'Unit': 'None'
                }
            ]
        )

        # Check for abnormal motion and send SNS alert
        if any(abs(a) > MOTION_THRESHOLD for a in [acceleration_x, acceleration_y, acceleration_z]):
            alert_message = f"🚨 Abnormal motion! Device: {device_id}\nX: {acceleration_x}\nY: {acceleration_y}\nZ: {acceleration_z}\nTime: {timestamp}"
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=alert_message,
                Subject="Abnormal Motion Alert!"
            )

        return {'statusCode': 200, 'body': json.dumps('Processing successful')}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Error: {str(e)}")}
