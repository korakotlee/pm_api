import os
from datetime import datetime
import io
import yaml
# import stringcase

from pathlib import Path

def make_file(path):
    json = {
        'method': 'get',
        'url': 'https://google.com',
    }
    with open(os.path.join(path, 'google.yaml'), 'w') as file:
        yaml.dump(json, file)

def run(path):
    print(f' *** PM API running ... {datetime.now()}\n')
    config_file = os.path.join(path,'config')
    if os.path.isfile(config_file):
        with open(config_file, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
    else:
        config = {
            'retry': 3,
            'limit': 10
        }
    for fi in os.listdir(path):
        if not fi.endswith(".yaml"):
            continue
        with open(os.path.join(path,fi), 'r') as file:
            json = yaml.load(file, Loader=yaml.FullLoader)
        if not json:
            print('.. skip invalid file: ', fi)
            continue
        print(json['url'])
    # make_file(path)


