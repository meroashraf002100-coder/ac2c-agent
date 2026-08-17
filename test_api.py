import requests

url = "https://ac2c-agent.vercel.app/generate"
payload = {"prompt": "Give me a quick JavaScript fetch example."}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print("Agent Response:\n")
        print(data.get("response"))
    else:
        print(f"Failed: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")