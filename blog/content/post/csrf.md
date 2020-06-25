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

# Defending against CSRF

* Identify where the request is coming from
  * Source and Target Origin Host
  * Origin rules
* CSRF Tokens - nonce value that is needs to be sent with the request

---

# Considerations

* CSRF for APIs?