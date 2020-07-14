---
title: "Same and Cross Origin Policy"
date: 2020-07-14T15:20:12+10:00

hiddenFromHomePage: false
postMetaInFooter: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""

---


# Same-Origin Policy (SOP)

* Javascript code can only access data from the same origin (scheme + host + port)
* Very limited access to cross-origin sites (unless server is configured to allow)

* Scripts, images, static files that remain relatively constant often are not protected by SOP
* Dynamic content is often protected by SOP


## JSONP (JSON with Padding)

JSONP is a technique to (legimately) fetch data from server on a different origin.  
This works due to the fact that content fetched through the `<script>` `src` tag attribute will be executed.  

JSONP is callback based.  
When the request to a JSONP endpoint is made, a function name that exists client-side is passed (i.e. as a parameter).  
The server will then perform the request, and return the response.  
The response is crafted in a way that the supplied callback function will be executed with the response as an argument.

i.e

```html
<script>
function receivedData(responseData) {
  alert("Received data: " + JSON.stringify(responseData));
}

<script src="https://api.myserver.com/jsonp?callbackFn=receivedData&data=5"></script>
```

The server's response to the request will look similar to the following
```
receivedData({"value": 5, "is-even": false})
```

## Allowing cross-origin

### Why Allow

* To allow API endpoints that are located on a different (sub)domain
* Scripts, images, content that is hosted on a different domain

### Headers

In order for cross-origin requests to work, the browser must receive several special headers from the server response

* `Access-Control-Allow-Origin` - List of origins allowed
* `Access-Control-Allow-Methods` - List of methods allowed
* `Access-Control-Allow-Headers` - List of non-standard headers
* `Access-Control-Max-Age` - Value in secs to cache preflight req

Browsers often request these headers through the OPTION method
