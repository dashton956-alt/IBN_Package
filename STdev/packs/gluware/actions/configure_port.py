import requests
import json
import sys

def run(serial, port_id, poe_enabled, api_url="http://wingpy:8080"):
    url = f"{api_url}/poe"
    payload = {
        "device_identifier": serial,
        "port_id": port_id,
        "operation": "enable" if poe_enabled else "disable"
    }
    resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
    resp.raise_for_status()
    return resp.json()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(json.dumps({"error": "missing args"}))
        sys.exit(2)
    serial = sys.argv[1]
    port_id = sys.argv[2]
    poe_enabled = sys.argv[3].lower() in ("true", "1", "yes")
    print(json.dumps(run(serial, port_id, poe_enabled)))
