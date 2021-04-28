import os
import json
import time
from datetime import datetime
# import pdb
import requests

def make_file(path):
    data = {
        'method': 'get',
        'url': 'https://google.com',
    }
    with open(os.path.join(path, 'google.json'), 'w') as file:
        json.dump(data, file)

def mkdir(path):
    dir = os.path.join(path, 'response')
    if not os.path.exists(dir):
        os.makedirs(dir)
        os.chmod(dir, 0o777)
    dir = os.path.join(path, 'success')
    if not os.path.exists(dir):
        os.makedirs(dir)
        os.chmod(dir, 0o777)
    dir = os.path.join(path, 'fail')
    if not os.path.exists(dir):
        os.makedirs(dir)
        os.chmod(dir, 0o777)


def run(path):
    print(f" *** PM 0.1 API running ... {datetime.now().strftime('%c')}\n")
    print('.. Process directory: ', path)
    mkdir(path)
    # make_file(path)
    config_file = os.path.join(path,'config')
    if os.path.isfile(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
    else:
        config = {
            'retry': 3,
            'limit': 10
        }
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
        for i in range(config['retry']):
            method = data['method']
            url = data['url']
            payload = data.get('data', None)
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
                }, f, indent=2)
            if response.ok:
                os.rename(req_file, os.path.join(path,'success', file))
                break
            else:
                if i == config['retry']:
                    # last time
                    os.rename(req_file, os.path.join(path,'fail', file))
            time.sleep(1/config['limit']*1.1)
