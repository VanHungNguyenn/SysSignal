from datetime import datetime

# Convert a datetime object to a Unix timestamp
def date_to_timestamp(date_check):
    timestamp = datetime.timestamp(date_check)
    return timestamp

# Convert a Unix timestamp to a datetime object
def timestamp_to_date(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object

# Get the current time as a datetime object
def time_now():
    result = datetime.now()
    ts = date_to_timestamp(result)
    new_result = timestamp_to_date(ts)
    return new_result
