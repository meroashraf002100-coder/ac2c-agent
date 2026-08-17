import requests

url = "https://ac2c-agent.vercel.app/generate"
payload = {"prompt": "Give me a quick JavaScript fetch example."}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")