import redshift_connector

import pandas as pd
from io import StringIO
import boto3 # For S3 operations

# --- Redshift Serverless and S3 Configuration (replace with your actual details) ---
AWS_REGION = 'ap-south-1' # Your AWS region
REDSHIFT_SERVERLESS_WORKGROUP_NAME = 'default-workgroup'
REDSHIFT_SERVERLESS_DB_NAME = 'dev' # Or your specific database name
# If using IAM Role for the executing environment (e.g., EC2, Lambda),
# you typically don't need access_key_id/secret_access_key here.
# redshift_connector will pick up credentials from env vars, ~/.aws/credentials, or IAM role.
# For local testing without an IAM role:
# AWS_ACCESS_KEY_ID = 'YOUR_AWS_ACCESS_KEY_ID'
# AWS_SECRET_ACCESS_KEY = 'YOUR_AWS_SECRET_ACCESS_KEY'

S3_KEY_PREFIX = 'serverless-data-uploads/'
# S3 bucket for COPY/UNLOAD (must exist and have Redshift role access)
S3_BUCKET_NAME = 'kkm2-unique-test-bucket-2025-06-26-py-1'
S3_FILE_TO_UNLOAD = 'redshift_sample.csv'
S3_UNLOAD_PATH = f's3://{S3_BUCKET_NAME}/{S3_FILE_TO_UNLOAD}'
S3_COPY_PATH = f's3://{S3_BUCKET_NAME}/flights.csv' # Path to your existing sample data

# IAM Role ARN for Redshift to access S3 (must have s3:GetObject on your bucket)
# This is attached to your Redshift Serverless namespace.
IAM_ROLE_ARN_FOR_COPY = 'arn:aws:iam::123456789012:role/YourRedshiftServerlessCopyRole'

def get_redshift_serverless_connection():
    """Establishes a connection to Amazon Redshift Serverless using IAM authentication."""
    try:
        conn = redshift_connector.connect(
            workgroup_name=REDSHIFT_SERVERLESS_WORKGROUP_NAME,
            database=REDSHIFT_SERVERLESS_DB_NAME,
            iam=True,
            region=AWS_REGION
            # ... other parameters
        )
        print("Successfully connected to Redshift Serverless!")
        return conn
    except Exception as e:
        print(f"Error connecting to Redshift Serverless: {e}")
        print("Ensure your AWS credentials are configured (e.g., via aws configure),")
        print("your security group allows access, and IAM permissions are correct.")
        return None

def list_redshift_databases(conn):
    """Lists all databases in the Redshift Serverless workgroup."""
    if not conn:
        print("No active connection to Redshift.")
        return []

    try:
        with conn.cursor() as cursor:
            # For Redshift Serverless, querying pg_database will show available databases within the namespace
            cursor.execute("SELECT datname FROM pg_database;")
            databases = [row[0] for row in cursor.fetchall()]
            print("\nRedshift Serverless Databases:")
            for db in databases:
                print(f"- {db}")
            return databases
    except Exception as e:
        print(f"Error listing databases: {e}")
        return []
get_redshift_serverless_connection()
