import boto3
import json

def lambda_handler(event, context):
    # Initialize the AWS Location Service client
    location_client = boto3.client('location')
    
    # Set your tracker and device IDs
    tracker_name = 'PetTracker'
    device_id = 'PetDevice'
    
    try:
        # Retrieve the device's position
        response = location_client.get_device_position(
            TrackerName=tracker_name,
            DeviceId=device_id
        )
        
        position = response.get('Position')
        if position and len(position) >= 2:
            longitude = position[0]
            latitude = position[1]
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Position data not available'})
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'longitude': longitude,
                'latitude': latitude
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
