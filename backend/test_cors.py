import requests

url = "https://langchainp5-ai-data-analyst.onrender.com/health"
headers = {
    "Origin": "https://ai-data-analyst-eta.vercel.app"
}

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"CORS Headers:")
print(f"  Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
print(f"  Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
print(f"  Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'NOT SET')}")
print(f"\nResponse: {response.json()}")
