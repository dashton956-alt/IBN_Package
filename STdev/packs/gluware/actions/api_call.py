import requests
import json
import sys

def run(method, path, api_url='https://demo.gluware.com', headers=None, params=None, body=None, token=None, timeout=30):
    method = method.upper()
    url = api_url.rstrip('/') + '/' + path.lstrip('/')
    hdrs = headers or {}
    hdrs.setdefault('Accept', 'application/json')
    if token:
        hdrs.setdefault('Authorization', f'Bearer {token}')
    try:
        if method == 'GET':
            resp = requests.get(url, headers=hdrs, params=params, timeout=timeout)
        elif method == 'POST':
            resp = requests.post(url, headers=hdrs, params=params, json=body, timeout=timeout)
        elif method == 'PUT':
            resp = requests.put(url, headers=hdrs, params=params, json=body, timeout=timeout)
        elif method == 'DELETE':
            resp = requests.delete(url, headers=hdrs, params=params, timeout=timeout)
        else:
            return {'error': f'Unsupported method {method}'}

        # Try to return JSON, fallback to text
        try:
            return resp.json()
        except ValueError:
            return {'status_code': resp.status_code, 'text': resp.text}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    # Simple CLI to test
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('method')
    p.add_argument('path')
    p.add_argument('--api_url', default='https://demo.gluware.com')
    p.add_argument('--token')
    args = p.parse_args()
    res = run(args.method, args.path, api_url=args.api_url, token=args.token)
    print(json.dumps(res))
