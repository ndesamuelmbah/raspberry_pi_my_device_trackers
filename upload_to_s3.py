import boto3, os

# Replace these with your own values
env = os.environ
bucket_name = env['BUCKET_NAME']
user_name = env['BOTO3_USER']


def upload_file_to_s3(local_file_path, debug=False):
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
    if debug:
        print(f'The file {local_file_path} has been uploaded to {s3_object_key} in {bucket_name}.')
