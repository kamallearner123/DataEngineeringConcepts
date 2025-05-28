import pandas
import os
import urllib.request as request
import tarfile
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing"
HOUSING_FILES = "housing.tgz"

HOUSING_URL = os.path.join(DOWNLOAD_ROOT, HOUSING_FILES)
print(HOUSING_URL)

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)
HOUSING_TGZ = os.path.join(DATA_PATH, "housing.tgz")

# Download tgz file
request.urlretrieve(HOUSING_URL, HOUSING_TGZ)

# Extract files
print(HOUSING_TGZ)
print(os.path.exists(HOUSING_TGZ))
tar_file = tarfile.open(HOUSING_TGZ)
tar_file.extractall(path="data/")
tar_file.close()

# Get list of files from "DATA_PATH"
files = os.listdir(DATA_PATH)
for file in files:
    if file.endswith(".csv"):
        file_path = os.path.join(DATA_PATH, file)
        df = pandas.read_csv(file_path)
        print(df.describe())
        print(df.info())

