import os
import json
import time
from datetime import datetime
import pdb
import requests
from requests_oauthlib import OAuth1Session
from pm_api import util

def init(path):

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
        o1 = data.get('oauth1', False)
        method = data['method']
        url = data['url']
        payload = data.get('payload', None)
        headers = data.get('headers', None)
        if o1:
            # OAuth1
            session = OAuth1Session(o1['key'], o1['secret'], o1['owner_key'], o1['owner_secret'])
            if method.lower() == 'get':
                response = session.get(url)
            if method.lower() == 'post':
                response = session.post(url, data=payload)
        else:
            # REST
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
        try:
            data['response'] = response.json()
        except Exception as e:
            data['response'] = response.text
        util.update_data(req_file, data)
        # if there's no callbacks, move to success/ or fail/

        # if there are callbacks that correspond to result
        # - set result to 'success' or 'fail'
        # - save the response
        # - move to callbacks
        # - then move to success/ or fail/ 

        if response.ok:
            callback_ok = data.get('callback_ok', False)
            if not callback_ok:
                os.rename(req_file, os.path.join(path,'success', file))
            else:
                data['result'] = 'ok'
                util.update_data(req_file, data)
                os.rename(req_file, os.path.join(path,'callback', file))
        else:
            if data['calls'] >= retry:
                # last time
                callback_fail = data.get('callback_fail', False)
                if not callback_fail:
                    os.rename(req_file, os.path.join(path,'fail', file))
                else:
                    data['result'] = 'fail'
                    data['response'] = response.json()
                    util.update_data(req_file, data)
                    os.rename(req_file, os.path.join(path,'callback', file))
