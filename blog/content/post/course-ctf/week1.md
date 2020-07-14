---
title: "Course CTF: Week 1"
date: 2020-06-03T19:07:45+10:00

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

## HTTP as a Service - Knowledge Base

Site: haas.-QBSITE-  
Scenario: Access to the `kb.-QBSITE-` site is IP restricted  
Solution: Use the `haas.-QBSITE-` proxy to enter HTTP messages  
Solution 2: Waste time and [create a forwarder](../../tools/kb_proxy)

```
GET / HTTP/1.1
Host: *redacted*

# HTTP/1.1 200 OK
# Accept-Ranges: bytes
# Content-Length: 94
# Content-Type: text/html; charset=utf-8
# Date: Mon, 01 Jun 2020 07:56:44 GMT
# Server: CTFProxy
# X-Ctfproxy-Trace-Context: b42e2d2a-3855-4ce6-ae18-d3b8e6816227
# 
# <a href="/c98efc0d-5c3f-45ec-996a-2cb82d35ed26.html">c98efc0d-5c3f-45ec-996a-2cb82d35ed26</a>
```

```
GET /c98efc0d-5c3f-45ec-996a-2cb82d35ed26.html HTTP/1.1
Host: *redacted*

# HTTP/1.1 200 OK
# Accept-Ranges: bytes
# Content-Length: 99
# Content-Type: text/html; charset=utf-8
# Date: Mon, 01 Jun 2020 07:57:53 GMT
# Server: CTFProxy
# X-Ctfproxy-Trace-Context: cf018b53-470c-4f6c-9128-441cec65e40f
# 
# <a href="/7643dc3d-2262-4f1c-8fb9-197860946a66.html">7643dc3d-2262-4f1c-8fb9-197860946a66.html</a>
# HTTP/1.1 400 Bad Request
# Content-Type: text/plain; charset=utf-8
# Connection: close
# 
# 400 Bad Request
```

```
GET /7643dc3d-2262-4f1c-8fb9-197860946a66.html HTTP/1.1
Host: *redacted*

# HTTP/1.1 200 OK
# Accept-Ranges: bytes
# Content-Length: 27
# Content-Type: text/html; charset=utf-8
# Date: Mon, 01 Jun 2020 07:57:26 GMT
# Server: CTFProxy
# X-Ctfproxy-Trace-Context: 92321514-00a0-41be-a05f-f69bdd6a8a02
# 
# COMP6443{I_CAN_WRITE_H11P}
```

> `COMP6443{I_CAN_WRITE_H11P}`

## HTTP as a Service - Knowledge Base Deep

Scenario: There is a bunch of circularly linked web pages, find the page with the flag  
Solution: Write a crawler to find the flag, ignore visited sites  
Solution File: [kb_deep.py](./kb_deep.py)

> `COMP6443{U_ARE_BA7MAN_1_AM_5P1DERMAN}`

## HTTP as a Service - Knowledge Base Human Calculator

Scenario: Complete 20 maths addition questions within two minutes  
Solution: Automate the calculation and submission of the questions  
Solution 2: Extract the answer from the JWT token and submit it  
Solution 3: Quick maffs  
Solution File: [kb_calculator.py](./kb_calculator.py)

> `COMP6443{SCR1PTING_1S_FUN}`

