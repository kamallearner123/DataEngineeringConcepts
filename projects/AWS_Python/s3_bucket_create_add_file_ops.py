import boto3
from botocore.exceptions import ClientError
import os

# --- Configuration ---
# Your S3 bucket name
S3_BUCKET_NAME = 'kkm-unique-s3-bucket-name-12345' # REPLACE THIS with your actual bucket name!
# The AWS region (us-east-1 as specified)
AWS_REGION = 'us-east-1' #us-east-1

# Initialize the S3 client
# boto3 automatically picks up credentials from environment variables or ~/.aws/credentials
s3_client = boto3.client('s3', region_name=AWS_REGION)

print(f"--- Connected to S3 in region: {AWS_REGION} ---")

# --- Function to check if a bucket exists ---
def bucket_exists(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            return False
        # Other errors like permission denied would still raise an exception
        raise

# --- 1. Create an S3 Bucket (Optional, if you don't have one yet) ---
# Note: Bucket names must be globally unique across all of AWS.
# Creating buckets might require specific IAM permissions.
print("\n--- Attempting to create bucket (if it doesn't exist) ---")
if not bucket_exists(S3_BUCKET_NAME):
    try:
        # Note: For us-east-1, LocationConstraint is not needed, but for other regions it is.
        # However, it's good practice to always specify it.
        # For us-east-1, LocationConstraint should be omitted or set to None
        if AWS_REGION == 'us-east-1':
            s3_client.create_bucket(Bucket=S3_BUCKET_NAME)
        else:
            s3_client.create_bucket(Bucket=S3_BUCKET_NAME,
                                    CreateBucketConfiguration={'LocationConstraint': AWS_REGION})
        print(f"Bucket '{S3_BUCKET_NAME}' created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")
        # Common errors: BucketAlreadyOwnedByYou, BucketAlreadyExists
        if 'BucketAlreadyOwnedByYou' in str(e) or 'BucketAlreadyExists' in str(e):
            print(f"Bucket '{S3_BUCKET_NAME}' already exists and is owned by you or another AWS account.")
        else:
            print(f"An unexpected error occurred during bucket creation: {e}")
else:
    print(f"Bucket '{S3_BUCKET_NAME}' already exists.")


# --- 2. Upload a File to S3 ---
print("\n--- Uploading a file to S3 ---")
local_file_name = "data/sample.txt"
s3_object_key = "data/documents/hello_s3.txt" # Path inside the bucket

# Create a dummy local file for upload
try:
    with open(local_file_name, "w") as f:
        f.write("This is some sample content for S3.\n")
        f.write("Welcome to the cloud!")
    print(f"Created local file: {local_file_name}")

    s3_client.upload_file(local_file_name, S3_BUCKET_NAME, s3_object_key)
    print(f"Successfully uploaded '{local_file_name}' to '{S3_BUCKET_NAME}/{s3_object_key}'")

except ClientError as e:
    print(f"Error uploading file: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Clean up the local dummy file
    if os.path.exists(local_file_name):
        os.remove(local_file_name)
        print(f"Removed local dummy file: {local_file_name}")

input("Check whether file is created or not!!!!")

# --- 3. List Files (Objects) in the S3 Bucket ---
print("\n--- Listing objects in the bucket ---")
try:
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
    if 'Contents' in response:
        print(f"Objects in bucket '{S3_BUCKET_NAME}':")
        for obj in response['Contents']:
            print(f"  - {obj['Key']} (Size: {obj['Size']} bytes, Last Modified: {obj['LastModified']})")
    else:
        print(f"No objects found in bucket '{S3_BUCKET_NAME}'.")
except ClientError as e:
    print(f"Error listing objects: {e}")

input("Check list of files in bucket")

# --- 4. Download a File from S3 ---
print("\n--- Downloading a file from S3 ---")
downloaded_local_file_name = "downloaded_s3_file.txt"

try:
    s3_client.download_file(S3_BUCKET_NAME, s3_object_key, downloaded_local_file_name)
    print(f"Successfully downloaded '{s3_object_key}' to '{downloaded_local_file_name}'")

    # Read and print content of the downloaded file
    with open(downloaded_local_file_name, "r") as f:
        content = f.read()
        print("\nContent of the downloaded file:")
        print(content)

except ClientError as e:
    print(f"Error downloading file: {e}")
    if e.response['Error']['Code'] == '404':
        print(f"The object '{s3_object_key}' does not exist in bucket '{S3_BUCKET_NAME}'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Clean up the downloaded local file
    if os.path.exists(downloaded_local_file_name):
        os.remove(downloaded_local_file_name)
        print(f"Removed local downloaded file: {downloaded_local_file_name}")
input("Check local_s3_bucket.txt is there or not")

# --- 5. Get File Content Directly (without saving to local disk) ---
print("\n--- Getting file content directly from S3 ---")
try:
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_object_key)
    file_content_bytes = response['Body'].read()
    file_content_str = file_content_bytes.decode('utf-8') # Decode if it's a text file
    print(f"Content of '{s3_object_key}':")
    print(file_content_str)
except ClientError as e:
    print(f"Error getting object content: {e}")
    if e.response['Error']['Code'] == 'NoSuchKey':
        print(f"The object '{s3_object_key}' does not exist in bucket '{S3_BUCKET_NAME}'.")

# --- 6. Delete a File from S3 (Use with Caution!) ---
print("\n--- Deleting a file from S3 ---")
# IMPORTANT: Only uncomment the following lines if you are absolutely sure you want to delete the file.
# This operation is irreversible!
# try:
#     s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_object_key)
#     print(f"Successfully deleted '{s3_object_key}' from '{S3_BUCKET_NAME}'")
# except ClientError as e:
#     print(f"Error deleting file: {e}")

# --- 7. Delete an S3 Bucket (Use with Extreme Caution!) ---
# A bucket must be empty before it can be deleted.
print("\n--- Deleting S3 bucket (if empty and you explicitly uncomment) ---")
# IMPORTANT: Only uncomment the following lines if you are absolutely sure you want to delete the bucket.
# This operation is irreversible!
# try:
#     if bucket_exists(S3_BUCKET_NAME):
#         # First, delete all objects in the bucket
#         response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
#         if 'Contents' in response:
#             for obj in response['Contents']:
#                 print(f"Deleting object: {obj['Key']}")
#                 s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=obj['Key'])
#             print("All objects deleted from bucket.")
#
#         s3_client.delete_bucket(Bucket=S3_BUCKET_NAME)
#         print(f"Bucket '{S3_BUCKET_NAME}' deleted successfully.")
# except ClientError as e:
#     print(f"Error deleting bucket: {e}")
#     if e.response['Error']['Code'] == 'BucketNotEmpty':
#         print("Bucket is not empty. Cannot delete bucket until all objects are removed.")
#     elif e.response['Error']['Code'] == 'NoSuchBucket':
#         print(f"Bucket '{S3_BUCKET_NAME}' does not exist.")
#     else:
#         print(f"An unexpected error occurred during bucket deletion: {e}")

print("\n--- S3 Operations Complete ---")
