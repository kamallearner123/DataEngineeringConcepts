import boto3
import os

print("Importing s3 utils!!!")
print("Module name is ", __name__)

# Upload file to s3 bucket
def upload_file(dir_name, file_name):
    print("Start: Uploading file to boto3")
    print(f"File Name: {file_name}")

    s3_client = boto3.client('s3')  # Service name
    LOCAL_FILE = dir_name+"/"+file_name
    REMOTE_FILE_PATH = "daniel/"+file_name

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    print("Bucket name read from env =", BUCKET_NAME)

    resp = s3_client.upload_file(LOCAL_FILE, 
                BUCKET_NAME,
                REMOTE_FILE_PATH)
    print("End: Uploading file to boto3")