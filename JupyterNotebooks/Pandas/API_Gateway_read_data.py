import requests
import pandas as pd

# Replace this with your actual API Gateway URL
api_gateway_url = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(api_gateway_url)
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json() # Parse the JSON response
        print("Successfully fetched data!")
        for i in data:
            print(i)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response content:", response.text)
