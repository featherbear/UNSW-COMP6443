---
title: "User Security"
date: 2020-06-15T17:00:18+10:00

description: "Authentication, Authorisation and Sessions"
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# The current state of security

> Authentication - Who are you.  
Authorisation - What can you do

* Currently, most websites are authenticated by a username and password combination.  
  * Many sites offer password reset functionality in the event that a user has forgotten their password
    * Email link
    * Secret question
* Some websites offer 2FA (SMS, Token, Apps, etc)
* Some websites offer delegated access (SSO, OAuth, JWT)
* CAPTCHA systems are occasionally implemented to to mitigate automated logins.

## Issues

* Password resets must be implemented securely, else they are in themselves a huge risk
  * A compromised email account will give an attacker access to your account through the link
  * Passwords sent in the header of an email can be read by malicious applications
  * Passwords sent in plain-text can be read by malicious applications
* Security Questions are dumb
  * Can you find the answers off Facebook
  * Can you find the answers off Google
  * How many times will the system allow you to enter incorrect answers
* Some websites are too verbose in their errors
  * Some sites return "Invalid username" and "Invalid password" messages
  * This disclosure could help an attacker to pinpoint a target
  * Just say invalid login!!!


<!-- LDAP and AD -> salted!

mimikatz -->

# HTTPS / SSL / TLS 

SSL/TLS encryption of requests and responses from and to the server. Generally prevents an attacker from (easily) intercepting communication.

# HTTPS Downgrade Attack

Force a client to communicate over HTTP so that an attacker can read requests from the client to the server. The MITM will make the HTTP connections to the server on behalf of the client.  

The attacker can intercept and modify content that comes from/goes to the client and server.

# HTTP Strict Transport Security (HSTS)

HSTS is a way of preventing HTTPS Downgrade attacks.  

Websites on the HSTS Preload list are required to use HTTPS, and the browser will refuse to go to the HTTP version of the site.

<!-- handshaking -->

# Tools: WiFi Pineapple

> Computer people sure like their fruits, eh?

A WiFi Pineapple is a miniature computer that is used to perform wireless reconnaissance and penetration attacks (i.e MITM)

---

# Authorisation

* Where is a user's access managed?
  * Don't store it client-side! We can modify these values!

---

# Sessions

HTTP is a stateless protocol, meaning that it does not inherently keep track of who we are, nor which requests belong to us.  

Several methods exist to keep track of our session: cookies, localStorage, sessionStorage, etcetera.

It is important to consider the security of sessions.  
Can they be tampered with? Forged?  
Can they be stolen through XSS, CSRF, etc?  
When we sign out, is the session actually destroyed?  
Does the session time out after a period of time?  

# Cookies

Browser cookies store pieces of data, that is transmitted to the server whenever make a request.

We could include some sort of identification (i.e a session ID) - which the server can store, to keep track of our visit.

i.e. A shopping cart associated with our session ID

Cookies can also contain other pieces of data - not just identifiers. We could store flags there, or our admin status - A bad idea, but entirely possible

## Cookie Security

To prevent cookies from being (easily) viewed and altered by Javascript code, we can set the `HTTP Only` flag in the cookie

