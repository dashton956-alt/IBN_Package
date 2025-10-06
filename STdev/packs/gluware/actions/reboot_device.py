import requests
import sys
import json

def run(serial, api_url="http://wingpy:8080"):
    url = f"{api_url}/api"
    payload = {"method": "POST", "endpoint": f"/devices/{serial}/reboot", "platform": "meraki"}
    resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
    resp.raise_for_status()
    return resp.json()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error": "missing serial"}))
        sys.exit(2)
    print(json.dumps(run(sys.argv[1])))
