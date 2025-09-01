import requests

# Test GET endpoint
response = requests.get("http://localhost:8050/generate/tiger")
print(response.json())

# Test POST endpoint
response = requests.post(
    "http://localhost:8050/generate",
    json={"animal": "shark"}
)
print(response.json())