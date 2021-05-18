import os
import json

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
