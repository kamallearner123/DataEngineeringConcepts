import boto3
import multiprocessing
s3_client = boto3.client('s3') # Service name
def print_bucket_names(s3_client):
    response = s3_client.list_buckets()
    for b in response["Buckets"]:
        print(b["Name"])

LOCAL_FILE = "Sample.txt"
REMOTE_FILE_PATH = "daniel/"

print_bucket_names(s3_client)

def uplaod_file(LOCAL_FILE):
    print("Local")
    resp = s3_client.upload_file(LOCAL_FILE, 
                                 'kkm2-unique-test-bucket-2025-06-26-py-1',
                                 REMOTE_FILE_PATH+LOCAL_FILE)
    print(resp)

LOCAL_FILES = ["Sample.txt", "Sample.txt", "Sample.txt", "Sample.txt"]

for file in LOCAL_FILES:
    uplaod_file(file)


with multiprocessing.Pool(processes=4) as pool:
    result = pool.map(uplaod_file, LOCAL_FILES)

print("End")