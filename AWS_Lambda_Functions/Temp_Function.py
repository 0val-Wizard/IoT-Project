import json
import boto3
import time
import calendar
from botocore.exceptions import ClientError
from datetime import datetime, timezone

def lambda_handler(event, context):
    try:
        print(f"Incoming event: {json.dumps(event)}")
        
        # Validate required fields
        required_fields = ['temperature', 'timestamp', 'device_id']
        if missing := [f for f in required_fields if f not in event]:
            return {
                'statusCode': 400,
                'body': f"Missing fields: {missing}"
            }

        temperature = float(event['temperature'])
        timestamp = event['timestamp']
        device_id = event['device_id']

        # Convert timestamp to UTC nanoseconds
        try:
            if isinstance(timestamp, (int, float)):
                epoch_time_ns = int(float(timestamp) * 1e9)
            else:
                # Use UTC-aware parsing
                dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
                epoch_seconds = int(dt.timestamp())
                epoch_time_ns = epoch_seconds * 1_000_000_000
                
            # Get current time in UTC
            now_ns = time.time_ns()  # Already returns UTC nanoseconds
            
            # Allow max 7-day future data (adjust as needed)
            max_future_ns = 7 * 86400 * 1_000_000_000
            if (epoch_time_ns - now_ns) > max_future_ns:
                return {
                    'statusCode': 400,
                    'body': f"Timestamp too far in future (max {7} days)"
                }
                
        except Exception as e:
            print(f"Timestamp error: {str(e)}")
            return {
                'statusCode': 400,
                'body': "Invalid timestamp format. Use ISO 8601 UTC (e.g., '2023-01-01T12:00:00')"
            }

        # Abnormal temperature check
        if not (35 <= temperature <= 39):
            sns = boto3.client('sns')
            sns.publish(
                TopicArn='arn:aws:sns:us-east-1:867344433481:Temperature_Alerts',
                Message=f'Abnormal temperature: {temperature}°C from {device_id}',
                Subject='Pet Temperature Alert'
            )

        # Write to Timestream
        timestream = boto3.client('timestream-write')
        try:
            response = timestream.write_records(
                DatabaseName='PetHealthMonitoring',
                TableName='TemperatureData',
                Records=[{
                    'MeasureName': 'temperature',
                    'MeasureValue': str(temperature),
                    'MeasureValueType': 'DOUBLE',
                    'Time': str(epoch_time_ns),
                    'TimeUnit': 'NANOSECONDS',
                    'Dimensions': [{'Name': 'DeviceID', 'Value': device_id}]
                }]
            )
            
            if response.get('RejectedRecords'):
                print(f"Rejection details: {json.dumps(response['RejectedRecords'], indent=2)}")
                return {
                    'statusCode': 400,
                    'body': "Timestream rejected records"
                }
                
        except ClientError as e: 
            print(f"Full error: {json.dumps(e.response, indent=2)}")
            rejected_records = e.response.get('RejectedRecords', [])
            print(f"Rejection reasons: {json.dumps(rejected_records, indent=2)}")
            return {
                'statusCode': 400,
                'body': f"Timestream write failed: {e.response['Error']['Message']}"
            }

        # CloudWatch metric
        cloudwatch = boto3.client('cloudwatch')
        cloudwatch.put_metric_data(
            Namespace='PetTemperature',
            MetricData=[{
                'MetricName': 'Temperature',
                'Dimensions': [{'Name': 'DeviceID', 'Value': device_id}],
                'Value': temperature,
                'Unit': 'None'
            }]
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Data processed successfully')
        }

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': "Internal processing error"
        }