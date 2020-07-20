---
title: "CSRF - Cross-Site Request Forgery"
date: 2020-06-22T17:14:01+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

> Allows an attacker to make a user perform an action.  

An attacker could craft a HTML page / request URI - that a victim would run.  

> i.e If a user visits the page `https://bankwebsite.com/pay?user=attacker&amount=100.00`, the user will pay the user `attacker` $100.

---

A payment probably won't happen as a GET request, but POST requests are still vulnerable!

The attacker could create a HTML page with a form that contains a submit button, and fields for `user=attacker` and `amount=100.00`. If the victim clicks on the button, they would submit that form!

In fact, if arbitrary HTML is able to be written - an attacker could even implement this as Javascript code (i.e `fetch`) - which means, as soon as the page is open, the POST request would be executed!

---

# Invalidated Redirect

What if a website has an auth callback (or even simply a redirect)

`http://website.com/login?redirect=http://website.com/home`

What if we changed `http://website.com/home` to `http://evil.com/hehe/?`????


# Response Splitting

```
resp["Location"] = "\r\nContent-Type: text/html\r\nSet-Cookie: ree=hahah\r\n\r\nehehehehhe"
```

# Defending against CSRF

* Identify where the request is coming from
  * Source and Target Origin Host
  * [Origin rules](../cross-origin-same-origin)
* CSRF Tokens - nonce value that is needs to be sent with the request
  * But these can be stolen with client-side code!
---

# Clickjacking

Hidden forms that are clicked on instead of the actual form control.

## Clickjacking vs Phishing

* Phishing involves creating an exact duplicate of the website
* Clickjacking involves loading the actual website, but adding elements which are clicked on instead

## Defense - Frame Buster

* Shows all frames

## Defense - NoScript

* Disable JS

## Defense - X-Frame Options

A website can send these headers in their response, to prevent those pages from being loaded as an `iframe`.

# Content Secure Policy (CSP)

Enforces the loading of information only from trusted locations

* HTTP Header
* `<meta>` Tag
* CSP report-only mode for monitoring
  * Adding a report URI will send a request to that URI when a violation occurs

* `frame-ancestors` - Only allow none/same site/certain domain to be loaded as a frame

### Nonce

Arbitrary numbers that are added to script tags to prove that they are trusted.  

* `nonce-NONCEVAL` - scripts with the nonce `NONCEVAL` are allowed to execute
* `strict-dynamic` - scripts with the nonce `NONCEVAL` that dynamically load other scripts are allowed to execute

# Considerations

* CSRF for APIs?
