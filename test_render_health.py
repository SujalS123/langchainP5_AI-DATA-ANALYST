import requests

print("Testing Render deployment...")
try:
    response = requests.get("https://langchainp5-ai-data-analyst.onrender.com/health", timeout=10)
    print(f"✓ Health check: {response.status_code}")
    print(f"  Response: {response.json()}")
    print(f"  CORS Header: {response.headers.get('access-control-allow-origin', 'NOT SET')}")
except Exception as e:
    print(f"✗ Health check failed: {e}")

print("\nTesting /files/list...")
try:
    response = requests.get("https://langchainp5-ai-data-analyst.onrender.com/files/list", timeout=10)
    print(f"✓ Files list: {response.status_code}")
    print(f"  CORS Header: {response.headers.get('access-control-allow-origin', 'NOT SET')}")
except Exception as e:
    print(f"✗ Files list failed: {e}")
