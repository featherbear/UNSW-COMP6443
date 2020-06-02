---
title: "KB Proxy"
date: 2020-06-02T17:01:42+10:00

description: "Automatically forward local-only sites through a tunnel endpoint"
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

# Introduction

**KB Proxy** is a [Burp](https://portswigger.net/burp) extension to access local-only sites through a tunnel endpoint.  
This allows you to directly access the KB site through your browser.

# Installation

* Download [Jython Standalone 2.7.2](https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar)
* Download [kb_proxy.py](../kb_proxy.py)

* In Burp Suite, go to the **[Extender] > [Options]** tab
  * Under **Python Environment** press **[Select file ...]**
  * Point to the downloaded [`jython-standalone-2.7.2.jar`](https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar)
  * Change the **Extension Type** to **Python**
* In Burp Suite, go to the **[Extender] > [Extensions]** tab
  * Under **Burp Extensions** press **[Add]**
  * Change the **Extension Type** to **Python**
  * Press **[Select file ...]** 
  * Point to the downloaded [`kb_proxy.py`](../kb_proxy.py)

# Configuration

Configuring the extension involves the editing of the `kb_proxy.py` file, followed by a reload of the extension (Unload and load again)

You can modify the `evaluateHeaders`, `HOST` and `TUNNEL` variables inside `kb_proxy.py`

## Boolean: evaluateHeaders

Whether or not to evaluate the response headers

## String: HOST

The hostname that will be forwarded

## String: TUNNEL

The endpoint to forward requests through

