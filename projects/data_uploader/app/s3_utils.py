import boto3

print("Importing s3 utils!!!")
print("Module name is ", __name__)


def upload_file(dir_name, file_name):
    print("Start: Uploading file to boto3")
    print(f"File Name: {file_name}")

    s3_client = boto3.client('s3')  # Service name
    LOCAL_FILE = dir_name+"/"+file_name
    REMOTE_FILE_PATH = "daniel/"+file_name

    resp = s3_client.upload_file(LOCAL_FILE, 
                'kkm2-unique-test-bucket-2025-06-26-py-1',
                REMOTE_FILE_PATH)
    print("End: Uploading file to boto3")