import requests

# Set your backend URL and parameters
url = "http://localhost:8000/feedback"
params = {
    "user_id": "testuser",   # Replace with your user ID
    "product_id": 1          # Replace with a valid product ID
}

# Send a POST request
response = requests.post(url, params=params)

# Print the response
print(response.status_code)
print(response.json())