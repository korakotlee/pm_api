import os
import json
import time
from datetime import datetime
import pdb
import requests
from pm_api import util

def init(path):

    RETRY = 3
    callback_dir = os.path.join(path,'callback')
    print('.. Process directory: ', callback_dir)
    for file in os.listdir(callback_dir):
        if not file.endswith(".json"):
            continue
        req_file = os.path.join(callback_dir,file)
        with open(req_file, 'r') as f:
            data = json.load(f)
        if not data:
            print('.. skip invalid file: ', file)
            continue
        result = data['result']
        callback_url = data.get('callback_'+result)
        print(callback_url)
        body = {
            "jsonrpc": "2.0",
            "method": "api",
            "id": 1,
            "params": data['response']
        }
        response = requests.post(callback_url, json=body)
        calls = data.get('callbacks', 0)
        data['callbacks'] = calls + 1
        util.update_data(req_file, data)

        if response.ok:
            os.rename(req_file, os.path.join(path,'success', file))
        else:
            if data['callbacks'] >= RETRY:
                os.rename(req_file, os.path.join(path,'fail', file))
