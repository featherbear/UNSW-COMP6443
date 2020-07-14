#!/usr/bin/python3

# Perform a directory crawl
# Manually tunnel the request through haas

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

def createReq(address):
    return urllib.parse.urlencode(dict(request=f"GET {address} HTTP/1.1\r\nHost: {FORWARD_HOST}"))

query = re.compile('a href="(.+?)"', re.MULTILINE)

seen = []
resps = []
queue = ["/deep/"]
while len(queue) > 0:
    next, queue = queue[0], queue[1:]
    if (next in seen):
        continue
    seen.append(next)
    data = createReq(next)
    print(data)
    req = requests.post(f'https://{TUNNEL_HOST}/', proxies=proxy, data=data, verify=False, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })
    resps.append(req.text)
    if "COMP" in req.text:
        print(req.text)
    baseURL = "/" + "/".join(next.split("/")[:-1][::-1])
    print(baseURL)
    queue = [*queue, *map(lambda link: (baseURL if link[0] == "." else "") + (link[2:] if link[0] == "." else link),    query.findall(req.text))]
print("Finish")
