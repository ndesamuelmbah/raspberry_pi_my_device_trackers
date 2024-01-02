import boto3, os, requests
from datetime import datetime, timedelta

# Replace these with your own values
env = os.environ
bucket_name = env['BUCKET_NAME']
user_name = env['BOTO3_USER']
post_header = env['POST_HEADER']


def upload_file_to_s3(local_file_path: str, post_time: datetime, debug: bool =False):
    '''Uploads a file to S3 to the path specified by BOTO3_USER saved on the device in environment variables.
    in the bucket specified by BUCKET_NAME fetched from environment variables.
    local_file_path: The path to the file to upload to S3.
    Exceptions: Throws an invalid argument exception if the file does not exist or BOTO3_USER or BUCKET_NAME are not set.
    Returns: None
    '''
    # Create an S3 client
    s3 = boto3.client('s3')
    # Uploads the given file using a managed uploader, which will split up large
    file_name = os.path.basename(local_file_path)

    s3_object_key = f'{user_name}/{file_name}'
    # Upload the file to S3
    s3.upload_file(local_file_path, bucket_name, s3_object_key)
    s3_base_url  = env['S3_BASE_URL']
    s3_url = f'{s3_base_url}/{s3_object_key}'

    if debug:
        print(f'The file {local_file_path} has been uploaded to {s3_object_key} in {bucket_name} with full url {s3_url}.')
    # write code to delete the file from the local file system
    os.remove(local_file_path)
    if debug:
        print(f'The file {local_file_path} has been deleted from the local file system.')
    # write code to make a POST request to the API Gateway endpoint
    post_url = env['POST_URL']
    post_data = {
        'sensorMediaData':
        {
            'dateTimeString': str(post_time),
            's3Url': s3_url,
            'userName': user_name,
            'email': env['EMAIL'],
            'description': "Samuel's Raspberry Pi Noticed A Motion Event."
        }
    }
    headers = { 'header': post_header}
    response = requests.post(post_url, headers=headers, json=post_data)
    if debug:
        print(f'The POST request to {post_url} returned {response.status_code} with the body {response.text}.')
