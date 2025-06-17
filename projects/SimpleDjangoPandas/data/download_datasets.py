'''
DATA_CATEGORIES = {
    "Sales": "sales",
    "Students": "students",
    "Titanic": "titanic",
    "Flights": "flights",
    "Iris": "iris",
    "Tips": "tips",
    "Diamonds": "diamonds",
    "Planets": "planets",
    "Insurance": "insurance",
    "Weather": "weather"
}'''
# Write code to download datasets from seaborn's repository
import os
import seaborn as sns

def download_datasets():
    datasets = [
        "titanic",
        "flights",
        "iris",
        "tips",
        "diamonds",
        "planets",
        "insurance",
        "weather"
    ]
    
    for dataset in datasets:
        try:
            data = sns.load_dataset(dataset)
            file_path = os.path.join("data", f"{dataset}.csv")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            data.to_csv(file_path, index=False)
            print(f"Downloaded and saved {dataset} dataset to {file_path}")
        except Exception as e:
            print(f"Failed to download {dataset} dataset: {e}")
if __name__ == "__main__":
    download_datasets()