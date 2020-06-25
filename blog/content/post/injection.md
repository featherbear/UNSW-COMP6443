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

## Techniques

* Add your own string escapes to your string to break the code
* Add comments (`--`) after the string escape to disable other parts of the SQL query

## OS-Interative Databases

If the database access files for ETL (extract, transform, load) operations, there may be vulnerabilities which allow us to read and write into the OS

* `LOAD DATA INFILE 'data.txt' INTO TABLE db2.my_table;`
* `SELECT LOAD_FILE('/tmp/world') AS world;`

It may even be possible to execute shell commands

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