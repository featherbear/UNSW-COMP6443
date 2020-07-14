FORWARD_HOST = ""
TUNNEL_HOST = ""

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import urllib
import re

proxy = {
  'https': 'http://127.0.0.1:8080',
  'http': 'http://127.0.0.1:8080'
}

for n in range(1, 9999+1):
    req = requests.get(f'https://blog.SITE/?p={n}', proxies=proxy, verify=False)
    if (req.status_code != 404):
        print(f"https://blog.SITE/?p={n}", flush=True)