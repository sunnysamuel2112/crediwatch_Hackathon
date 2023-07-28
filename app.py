import boto3
from botocore.exceptions import ClientError

# Set up S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id='',
    aws_secret_access_key=''
)

# Specify the bucket name
data_bucket_name = 'rules-engine-data'

# Retrieve the list of files in the bucket
try:
    response = s3.list_objects_v2(Bucket=data_bucket_name)
    files = response['Contents']
except ClientError as e:
    print(f"Error retrieving the list of files: {str(e)}")
    # Handle the error appropriately

# Loop through the files and retrieve the desired file
data_file_name = ''  # Initialize with an empty string
if 'files' in locals():
    for file in files:
        if file['Key'].endswith('.json'):
            data_file_name = file['Key']
            break

if data_file_name:
    try:
        data_obj = s3.get_object(Bucket=data_bucket_name, Key=data_file_name)
        data_content = data_obj['Body'].read().decode('utf-8')
        print(data_content)
    except ClientError as e:
        print(f"Error reading data file: {str(e)}")
        # Handle the error appropriately
else:
    print("No JSON data file found in the bucket.")
    # Handle the case when no JSON data file is found

# Read rules JSON
rules_file_name = 'rules.json'
try:
    rules_obj = s3.get_object(Bucket=data_bucket_name, Key=rules_file_name)
    rules_content = rules_obj['Body'].read().decode('utf-8')
except ClientError as e:
    print(f"Error reading rules JSON: {str(e)}")
    # Handle the error appropriately
