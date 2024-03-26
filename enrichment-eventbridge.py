import json

def lambda_handler(event, context):
    filtered_records = []

    # Ensure event is a list and has at least one element
    if isinstance(event, list) and event:
        # Iterate through each event
        for event_data in event:
            print("Event is:", event_data)
            
            # Extracting the body from the event data
            body_str = event_data.get('body', '')  # Get the body as a string
            
            # Parse the body string into a dictionary
            try:
                body = json.loads(body_str)
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                continue
            
            # Extracting start date and end date from the body
            start_date = body.get('startDate')
            end_date = body.get('endDate')
            
            # Checking if start date and end date are present and start date is less than or equal to end date
            if start_date and end_date and start_date <= end_date:
                # Checking if start date != end date (booking duration more than 1 day)
                if start_date != end_date:
                    filtered_records.append(body)  # Append the message if booking duration > 1 day
            else:
                print("Invalid date range:", start_date, end_date)

    else:
        print("Event is not in the expected format")

    return filtered_records
