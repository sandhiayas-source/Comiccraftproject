import requests

BASE_URL = "http://127.0.0.1:8000"

# Check API status
response = requests.get(
    f"{BASE_URL}/health",
    timeout=10
)
response.raise_for_status()

# Test data
user_data = {
    "name": "Arun",
    "email": "arun@example.com",
    "age": 21
}

# Create user
response = requests.post(
    f"{BASE_URL}/api/users",
    json=user_data,
    timeout=30
)
response.raise_for_status()

result = response.json()

assert result["name"] == "Arun"
assert result["age"] == 21

print("User API smoke test passed.")
