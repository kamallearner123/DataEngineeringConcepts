#import psycopg2

print("Importing s3 utils!!!")
print("Module name is ", __name__)

# --- RDS Connection Details (REPLACE WITH YOURS) ---
DB_HOST = "replace with API" # e.g., my-python-db-instance.xxxx.ap-south-1.rds.amazonaws.com
DB_PORT = 5432 # Default for PostgreSQL
DB_NAME = "mydb" # The initial database name you set (or 'postgres' if you didn't)
DB_USER = "postgres" # Your master username
DB_PASSWORD = "xxx" # Your master password


def get_conn():
    # try:
    #     conn = psycopg2.connect(
    #         host=DB_HOST,
    #         port=DB_PORT,
    #         database=DB_NAME,
    #         user=DB_USER,
    #         password=DB_PASSWORD
    #     )
    #     print("Successfully connected to Amazon RDS (PostgreSQL)!")
    #     return conn
    # except:
    #      return None
    pass

def create_table(conn):
    pass

def upload_data_to_rds(csv_file):
    print("Start: Going to upload data to RDS")
    print(f"File Name: {csv_file}")
    conn = get_conn()
    create_table(conn)
    print("Stop: Going to upload data to RDS")    