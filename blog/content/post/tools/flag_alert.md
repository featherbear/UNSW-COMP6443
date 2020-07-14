---
title: "Flag Alert"
date: 2020-06-23T10:03:10+10:00

categories: ["Tools"]
hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---

> Imagine doing a CTF challenge, and you're trying to find a flag; but you don't realise that you've found it already. And so you waste time figuring out other ways to try to get it - but you've already found it - that was me. Oops.

# Introduction


**Flag Alert** is a [Burp](https://portswigger.net/burp) extension that checks the HTTP responses for CTF flags.  
It will highlight the packets which contain flags, and also alert you when new flags are found.

# Installation

* Download [Jython Standalone 2.7.2](https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar)
* Download [flag_alert.py](../flag_alert.py)

* In Burp Suite, go to the **[Extender] > [Options]** tab
  * Under **Python Environment** press **[Select file ...]**
  * Point to the downloaded [`jython-standalone-2.7.2.jar`](https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar)
  * Change the **Extension Type** to **Python**
* In Burp Suite, go to the **[Extender] > [Extensions]** tab
  * Under **Burp Extensions** press **[Add]**
  * Change the **Extension Type** to **Python**
  * Press **[Select file ...]** 
  * Point to the downloaded [`flag_alert.py`](../flag_alert.py)
