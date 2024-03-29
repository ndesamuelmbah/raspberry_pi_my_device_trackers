import boto3, os, requests, cv2
from datetime import datetime, timedelta
from itertools import permutations

# Replace these with your own values
env = os.environ
bucket_name = env['BUCKET_NAME']
user_name = env['BOTO3_USER']
post_header = env['POST_HEADER']
motion_header = env['MOTION_HEADER']
email = env['EMAIL']
dates_file = 'dates.txt'

#net = cv2.dnn.readNetFromTensorflow('ssd_mobilenet_v1_coco/frozen_inference_graph.pb', 'ssd_mobilenet_v1_coco.pbtxt')


def notify_motion_detected(debug: bool = False):
    '''Sends a POST request to the API Gateway endpoint to notify of a motion event.
    Exceptions: Throws an invalid argument exception if BOTO3_USER or BUCKET_NAME are not set.
    Returns: None
    '''
    dates = []
    with open(dates_file, 'r') as f:
        dates = f.read().splitlines()
        f.close()
    if len(dates) > 0 and (datetime.now() - datetime.strptime(dates[-1], '%Y-%m-%d %H:%M:%S.%f')).total_seconds() < 9:
        if debug:
            print('Already notified this.')
        return None

    post_url = env['POST_URL']
    post_data = {
        'sensorMediaData':
        {
            'isMotionDetected': 'yes',
            'dateTimeString': str(datetime.utcnow()),
            'userName': user_name,
            'email': email,
            'description': motion_header
        }
    }
    headers = { 'header': post_header}
    response = requests.post(post_url, headers=headers, json=post_data)
    if debug:
        print(f'The POST request to {post_url} returned {response.status_code} with the body {response.text}.')
    with open(dates_file, 'w') as f:
        f.write(str(datetime.now()))
        f.close()


def upload_file_to_s3(local_file_path: str, post_time: datetime, debug: bool = False):
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
    s3_url = f'{s3_base_url}{s3_object_key}'

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
            'isMotionDetected': 'no',
            'dateTimeString': str(post_time),
            's3Url': s3_url,
            'userName': user_name,
            'email': email,
            'description':  motion_header
        }
    }
    headers = { 'header': post_header}
    response = requests.post(post_url, headers=headers, json=post_data)
    if debug:
        print(f'The POST request to {post_url} returned {response.status_code} with the body {response.text}.')
