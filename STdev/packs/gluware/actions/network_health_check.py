import requests
import json
import sys

def run(organization_id, api_url="http://monitoring-glueware:3000", token=None):
    url = f"{api_url}/api/health-check"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = requests.get(url, params={"org_id": organization_id, "include_devices": True, "include_clients": True}, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error": "missing organization_id"}))
        sys.exit(2)
    print(json.dumps(run(sys.argv[1])))
