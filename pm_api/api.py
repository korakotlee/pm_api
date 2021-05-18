import os
import json
import time
from datetime import datetime
import pdb
import requests
from requests_oauthlib import OAuth1Session
from pm_api import process_request
from pm_api import process_callback

def run(path):
    print(f" *** PM 0.2 API running ... {datetime.now().strftime('%c')}\n")
    process_request.init(path)
    process_callback.init(path)
        

if __name__ == "__main__":
    run('/var/api')

