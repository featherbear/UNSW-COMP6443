---
title: "Tutorial 7 Notes"
date: 2020-07-15T17:01:45+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

* Victim is now the client
* Payload executes against the user instead of the server

# Same Origin Policy (SOP)

Two sites with the same origin have the same **scheme**, **port** and **host**.  

* SOP restricts where resources can be loaded from.
* SOP usually does not apply to static content
* SOP usually applies to resources, like Javascript, Cookies, AJAX

## CORS Headers

Headers that are sent by the server, which dictate where resources can be loaded from

# Cross Site Scripting (XSS)

Useful Site: [requestbin.com](https://requestbin.com)

* Blacklists are 'easy' to defeat - just find an attack vector that isn't on the blacklist
