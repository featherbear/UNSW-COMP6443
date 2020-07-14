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



def generate():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(3))

base = "6fbRN72"

def tryString(addr):
    return requests.get("https://support.SITE/raw/" + addr, proxies=proxy, verify=False).status_code != 404

# result = False
# for x in range(len(base)):
#     addr = list(base)
#     for y in string.ascii_letters + string.digits:
#         addr[len(addr) - x - 1] = y
#         if tryString("".join(addr)):
#             break

result = False
while not result:
    result = tryString("6fbR" + generate())