import json
import boto3
from decimal import Decimal

# Initialize AWS clients
location_client = boto3.client('location')
dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')

# Constants for tracker and DynamoDB table
TRACKER_NAME = "PetTracker"
TABLE_NAME = "GPSDataTable" 
DEVICE_ID = "PetDevice"

# DynamoDB table reference
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print("Event received from IoT:", json.dumps(event, indent=2))
    
    # Extract coordinates and timestamp directly from the event
    coordinates = event.get('coordinates')
    timestamp = event.get('timestamp')
    
    if coordinates and timestamp:
        # Convert coordinates to Decimal for DynamoDB
        latitude = Decimal(str(coordinates[1]))  # Convert to Decimal
        longitude = Decimal(str(coordinates[0]))  # Convert to Decimal
        
        # Save data to DynamoDB
        table.put_item(Item={
            'DeviceId': DEVICE_ID,
            'Timestamp': timestamp,
            'Latitude': latitude,  # Keep as Decimal
            'Longitude': longitude  # Keep as Decimal
        })
        
        # Publish custom metric to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='PetTracker',
            MetricData=[
                {
                    'MetricName': 'GPSLocationUpdates',
                    'Dimensions': [
                        {'Name': 'DeviceId', 'Value': DEVICE_ID}
                    ],
                    'Timestamp': timestamp,
                    'Value': 1,  # Each update increments the metric
                    'Unit': 'Count'
                }
            ]
        )
        
        # Convert to float for Location Service compatibility
        latitude_float = float(latitude)
        longitude_float = float(longitude)
        
        # Update location in AWS Location Service Tracker
        try:
            response = location_client.batch_update_device_position(
                TrackerName=TRACKER_NAME,
                Updates=[
                    {
                        'DeviceId': DEVICE_ID,
                        'Position': [longitude_float, latitude_float],  # Use float here
                        'SampleTime': timestamp  # Sample time in ISO 8601 format or Unix timestamp
                    }
                ]
            )
            print("Tracker update response:", response)
        except Exception as e:
            print("Error updating tracker:", e)
    else:
        print(f"Invalid GPS data received: {event}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Message processed and stored successfully!')
    }
