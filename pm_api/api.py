import os
import json
import time
from datetime import datetime
# import pdb
import requests

def make_sample_file(path):
    data = {
        'method': 'get',
        'url': 'https://google.com',
        'callback_ok': 'http://localhost:8069/api/test/ok',
        'callback_fail': 'http://localhost:8069/api/test/fail',
        'payload': {
            'id': 123,
            'name': 'test'
        },
        'retry': 3,
        'limit': 5,
    }
    with open(os.path.join(path, 'google.json'), 'w') as file:
        json.dump(data, file, indent=4)

def run(path):
    print(f" *** PM 0.1 API running ... {datetime.now().strftime('%c')}\n")
    print('.. Process directory: ', path)
    for file in os.listdir(path):
        if not file.endswith(".json"):
            continue
        req_file = os.path.join(path,file)
        with open(req_file, 'r') as f:
            data = json.load(f)
        if not data:
            print('.. skip invalid file: ', file)
            continue
        print(data['url'])
        retry = data.get('retry', 5)
        limit = data.get('limit', 5)
        method = data['method']
        url = data['url']
        payload = data.get('payload', None)
        headers = data.get('headers', None)
        if method.lower() == 'get':
            response = requests.get(url, headers=headers)
        if method.lower() == 'post':
            response = requests.post(url, data=payload, headers=headers)
        response_file = os.path.join(path, 'response', file+'_'+str(response.status_code)+ '_'+
            str(datetime.now().strftime('%Y%m%d_%H%M%S')))
        with open(response_file, 'w') as f:
            if response.headers['content-type'].startswith('application/json'):
                json_data = response.json()
            else:
                json_data = {}
            json.dump( {
                'url': response.url,
                'headers': dict(response.headers),
                'json': dict(json_data),
                'text': response.text,
            }, f, indent=4)
        calls = data.get('calls', 0)
        data['calls'] = calls + 1
        with open(os.path.join(req_file), 'w') as f:
            json.dump(data, f, indent=4)
        if response.ok:
            os.rename(req_file, os.path.join(path,'success', file))
            if data.get('callback_ok', False):
                requests.post(data['callback_ok'], data=response.text)
        else:
            if data.get('callback_fail', False):
                requests.post(data['callback_fail'], data=response.text)
            if data['calls'] >= retry:
                # last time
                os.rename(req_file, os.path.join(path,'fail', file))
            time.sleep(1/limit*1.1)
