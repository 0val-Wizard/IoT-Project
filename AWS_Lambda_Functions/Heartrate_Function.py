import json
import boto3
import os
from botocore.exceptions import ClientError
from decimal import Decimal

# Initialize AWS clients
sagemaker = boto3.client('runtime.sagemaker')
iot = boto3.client('iot-data', region_name='us-east-1')  
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('HeartRateData')

SAGEMAKER_ENDPOINT = 'sagemaker-xgboost-2025-02-02-03-05-19-383' 
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:867344433481:HeartRate_Alerts'
IOT_TOPIC = 'pawtracker/heartrate'

def lambda_handler(event, context):
    try:
        # Extract heart rate data from the event
        heart_rate = int(event['heart_rate'])
        timestamp = Decimal(str(event['timestamp'])) 
        pet_id = event.get('pet_id', 'unknown')
        weight = Decimal(str(event.get('weight', 10.0)))
        age = int(event.get('age', 5))
        ecg_mean = Decimal(str(event.get('ecg_mean', 75)))
        ecg_max = Decimal(str(event.get('ecg_max', 100)))
        ecg_min = Decimal(str(event.get('ecg_min', 50)))
        total_bad_duration = Decimal(str(event.get('total_bad_duration', 0)))
        first_hr_value = Decimal(str(event.get('first_hr_value', 72)))

        # Prepare payload for SageMaker model
        payload = f"{weight},{age},{heart_rate},{ecg_mean},{ecg_max},{ecg_min},{total_bad_duration},{first_hr_value}"

        # Call SageMaker Model
        response = sagemaker.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT,
            ContentType="text/csv",
            Body=payload
        )

        # Read and process response from SageMaker
        body = response['Body'].read().decode().strip()
        print(f"Raw SageMaker Response: {body}")

        try:
            prediction = Decimal(body)  
        except ValueError:
            print(f"Unexpected response from SageMaker: {body}")
            prediction = Decimal('0') 

        abnormal_heart_rate = prediction > Decimal('0.5') 

        # Send SNS alert if abnormal heart rate is detected
        if abnormal_heart_rate:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f'Abnormal heart rate detected: {heart_rate} BPM for pet {pet_id}. Check on your pet!',
                Subject='Pet Heart Rate Alert'
            )

        # ✅ Store ALL Data in DynamoDB (Retrieval Capability Added)
        item = {
            'timestamp': timestamp,
            'pet_id': pet_id,
            'heart_rate': heart_rate,
            'weight': weight,
            'age': age,
            'ecg_mean': ecg_mean,
            'ecg_max': ecg_max,
            'ecg_min': ecg_min,
            'total_bad_duration': total_bad_duration,
            'first_hr_value': first_hr_value,
            'prediction': prediction
        }

        table.put_item(Item=item)
        print("✔ Data successfully stored in DynamoDB.")

        # ✅ Retrieve last recorded heart rate for debugging
        response = table.get_item(Key={'timestamp': timestamp, 'pet_id': pet_id})
        retrieved_data = response.get('Item', {})
        print(f"Retrieved from DynamoDB: {json.dumps(retrieved_data, default=str)}")

        # ✅ Publish to AWS IoT Core
        iot_payload = {
            'timestamp': str(timestamp),  
            'pet_id': pet_id,
            'heart_rate': heart_rate,
            'prediction': float(prediction)  
        }
        iot.publish(topic=IOT_TOPIC, qos=1, payload=json.dumps(iot_payload))
        print("✔ IoT message published.")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Heart rate processed successfully', 'prediction': float(prediction)})
        }

    except ClientError as e:
        print(f"AWS ClientError: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'AWS ClientError', 'details': e.response['Error']['Message']})
        }
    except Exception as e:
        print(f"Unhandled Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)})
        }
