---
title: "Attacking Web Apps"
date: 2020-06-21T14:33:04+10:00

description: "An insight into security assessment"
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

[Wappalyzer]: https://www.wappalyzer.com/

> Website security assessment can be very daunting - there are so many different tools and technologies that you need to know, that it can often be overwhelming to find out where to start.  
&nbsp;  
This article covers some insights, tips and tricks on tackling web application security.  
It's no step-by-step guide of any sort, but it will definitely be useful to consider the things mentioned whenever you analyse a new web app.

---

# Know your Web App

Before you attack web apps, you _first_ need to **know your app**.  

* What software is the server using?  
* What libraries does the software use?
* What is the version of the software/library?

---

> It definitely helps to have personal experience with various web application frameworks - as these previous experiences will help guide you during your analysis. You'll know what is normal and what is not, and you'll be able to ignore components of the website that are so-called 'red-herrings' in your assessment.

It is important to know what the server is comprised of.  
By identifying the technologies use in the application, they may lead to valuable clues.

Knowing the software versions of the server and library can also be beneficial.  
Often, security vulnerabilities are discovered and fixed in a future release, protecting whoever has updated from that vulnerability - but **you won't believe how many websites continue to use outdated versions of software**. By knowing the versions of the software use, we may be able to find vulnerabilities that still affect the web app.

---

There are several ways to get a picture of what the server uses.  

* Browsing the website for contextual clues
* Looking at the source code to find common patterns
* Looking at the HTTP response headers for any server software name
* [Wappalyzer]

[Wappalyzer] is a browser extension that uses artifacts in the content from the server to identify the software and libraries (and their version) used in the web application. It won't always be useful, but more times than not it will give you an overview of possible ways to assess the web app.

---

When you find out the technologies used in the web app, you can then consider what types of attack vectors (methods) to try.

As example, for a website that uses Wordpress...

* Wordpress is written in the PHP language
  * Find any vulnerabilities for the version of PHP used
  * Find any vulnerabilities for the version of Wordpress used
* Wordpress is a content management system, with users, pages, posts...
  * Find the users, pages, media, content (enumeration)
* ALL Wordpress sites have a `/wp-login` and `/wp-admin` page
* Wordpress uses a SQL database
  * Can we access this database?

Another example, a website that uses Flask...

* Flask servers have a debug mode that grants a client a shell if they log in with the debug password
  * Is the server running on debug mode?
  * Can we brute force the password?
* Secure data (i.e. encrypted cookies) stored in the client
  * Does the application leak the secret key that is used to encrypt the data?
  * Can we modify the data?

---

Then look for common files that may exist on the website...
For example: `robots.txt`, `humans.txt`, `sitemap.xml`  
These files can provide useful information.

You may also like to perform directory / (sub)domain / content enumeration, to find any resources that are hidden but exist.  
i.e. use a wordlist (dictionary)

# Know your Attack Vectors

Once you know the technologies and structures used in the server, you can consider how to approach attacking the system.

* Payloads (queries in a GET request, bodies in a POST request) could be intercepted and modified to get a desired outcome

* Cookies store pieces of data stored in the client which the server uses - these could be potentially modified.

* [JSON Web Tokens](https://jwt.io/) contain claims (pieces of data).  
Whilst they are **NOT** designed to encrypt / hide data, they are designed to verify the integrity of the data (whether it has been tampered with or not).  
If the server does not perform a 'signature verification' when parsing a JWT token, a tampered token would be accepted by the server, giving us an attack vector.

* Flask Secure Cookies basically mirror the functionality of JWT tokens (data verification and integrity over data privacy), but are used as part of a [Flask](https://flask.palletsprojects.com) application. If the secret key of a Flask application is known, it is possible to falsify claims and sign it, as if it was legitimate.

* SQLi (SQL Injection) - If a server is using some database in the backend, and there is a means for the server to parse received data, it may be possible to trick the server into running arbitrary operations.

* Login bruteforce / enumeration

# Know your Tools

* Proxy / Interceptor - These tools help you to view messages sent to and from the server, and allow you to modify them
* Developer Console - The developer console in your browser can view page elements, network requests, cookies, storages
* [CyberChef](https://gchq.github.io/CyberChef/) - An feature-rich solution for playing around with data
* [Wappalyzer] - Identify technologies used in websites

