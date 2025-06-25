import requests

# Example: API Key (replace 'YOUR_API_KEY' with your actual key)
headers = {
    "x-api-key": "YOUR_API_KEY", 
    "Content-Type": "application/json"
}

# For this demo, the placeholder API doesn't use API keys, 
# so we'll use a different endpoint that accepts query parameters.
api_gateway_url_with_params = "https://jsonplaceholder.typicode.com/comments"

try:
    # Make the request with headers
    # In a real scenario, this URL would be your API Gateway endpoint requiring the key
    response_with_headers = requests.get(api_gateway_url_with_params, headers=headers)
    response_with_headers.raise_for_status()
    print("Request with headers successful (if API supported it)!")
    print(response_with_headers.json()[:1]) # Uncomment to see response

except requests.exceptions.RequestException as e:
    print(f"Error making request with headers: {e}")

import pandas as pd
df = pd.DataFrame(response_with_headers.json())
print(df.head())
df.describe()
