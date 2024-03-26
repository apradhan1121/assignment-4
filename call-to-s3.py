import json
import boto3
import csv
from io import StringIO

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Ensure event is a list and has at least one element
    if isinstance(event, list) and event:
        # Extracting the first element from the list
        event_data = event[0]
        print("Event is:", event_data)
        
        # Extracting the booking details directly from the event data
        booking_details = event_data
        
        print("Booking Details:", booking_details)  
        
        # Convert booking details to CSV format
        csv_data = convert_to_csv(booking_details)
        print("CSV Data:", csv_data)  
        
        # Writing CSV data to S3
        bucket_name = 'output-filtered-records'  
        file_key = 'filtered_bookings.csv'  
        
        # Append CSV data to the file in S3
        append_csv_data_to_s3(bucket_name, file_key, csv_data)
        
        return {
            'statusCode': 200,
            'body': 'Filtered records processed and written to S3 successfully'
        }
    else:
        return {
            'statusCode': 400,
            'body': 'Event data is not in the expected format'
        }

def convert_to_csv(data):
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=data.keys())
    
    # Write header if file doesn't exist
    if csv_buffer.tell() == 0:
        writer.writeheader()
    
    # Write data
    writer.writerow(data)
    
    return csv_buffer.getvalue()

def append_csv_data_to_s3(bucket_name, file_key, csv_data):
    try:
        # Read existing CSV data from S3
        existing_csv_data = ''
        if file_exists_in_bucket(bucket_name, file_key):
            existing_object = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            existing_csv_data = existing_object['Body'].read().decode('utf-8')
        
        # Concatenate existing CSV data with new CSV data
        updated_csv_data = existing_csv_data + csv_data
        
        # Write updated CSV data to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=updated_csv_data.encode('utf-8'),
            ContentType='text/csv',
            ContentDisposition='attachment',
            ACL='bucket-owner-full-control'
        )
    except Exception as e:
        print(f"Error appending CSV data to S3: {e}")

def file_exists_in_bucket(bucket_name, file_key):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=file_key)
        return True
    except:
        return False
