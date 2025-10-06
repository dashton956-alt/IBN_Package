import requests
import sys
import json

def run(serial, api_url="http://wingpy:8080", api_key=None):
    url = f"{api_url}/device-info"
    payload = {"device_identifier": serial}
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()

if __name__ == '__main__':
    # StackStorm python-script runner calls run() but we provide CLI fallback
    args = sys.argv[1:]
    if not args:
        print(json.dumps({"error": "missing serial"}))
        sys.exit(2)
    result = run(args[0])
    print(json.dumps(result))
