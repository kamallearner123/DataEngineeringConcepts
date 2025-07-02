import os
import json
from app import s3_utils
from app import rds_utils

print("Importing core!!!")
print("Module name is ", __name__)

def add(a,b):
    return a+b

def main_core():
    # Read the files from a directory
    # If file ends with .csv, upload to RDS
    # If file ends with .txt, upload to s3 bucket
    print(os.getcwd())
    fd = open("config.json")
    local_directory = json.load(fd)["local_directory"]
    
    files = os.listdir(local_directory)
    for file in files:
        if file.endswith(".csv"):
            rds_utils.upload_data_to_rds(local_directory+"/"+file)
        else:
            s3_utils.upload_file(dir_name = local_directory, file_name = file)