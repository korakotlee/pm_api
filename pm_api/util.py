import os
import json

def update_data(req_file, data):
    with open(os.path.join(req_file), 'w') as f:
        json.dump(data, f, indent=4)
