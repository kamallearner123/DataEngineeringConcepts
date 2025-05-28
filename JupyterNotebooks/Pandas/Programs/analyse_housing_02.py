"""Script to download, extract, and analyze the California housing dataset."""
import os
import tarfile
from urllib import request
import pandas as pd

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing"
HOUSING_FILES = "housing.tgz"
HOUSING_URL = os.path.join(DOWNLOAD_ROOT, HOUSING_FILES)
print(HOUSING_URL)

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)
HOUSING_TGZ = os.path.join(DATA_PATH, "housing.tgz")

request.urlretrieve(HOUSING_URL, HOUSING_TGZ)

print(f"File path: {HOUSING_TGZ}")
print(f"File exists: {os.path.exists(HOUSING_TGZ)}")
try:
    with tarfile.open(HOUSING_TGZ, "r:*") as tar_file:
        tar_file.extractall(path=DATA_PATH)
    print(f"Extracted {HOUSING_TGZ} to {DATA_PATH}")
except tarfile.ReadError as e:
    print(f"Error extracting file: {e}")

# Load and analyze the dataset
csv_path = os.path.join(DATA_PATH, "housing.csv")
try:
    housing = pd.read_csv(csv_path)
    print(housing.head())
except FileNotFoundError:
    print(f"Error: {csv_path} not found. Check extraction.")

