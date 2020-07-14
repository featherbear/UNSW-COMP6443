---
title: "Course CTF: DNS Recon"
date: 2020-06-01T13:45:35+10:00

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

# Useful Tools and Resources

## [SecLists](https://github.com/danielmiessler/SecLists)

SecLists is a giant repository of useful word lists and payloads for use with various other tools!

## [gobuster](https://github.com/OJ/gobuster)

Gobuster is a dictionary-based directory, DNS and Virtual Host enumerator

* `../gobuster dns -d [DOMAIN] -w wordlist.txt -t 50 -o wordlist_scan.txt`

## [altdns](https://github.com/infosec-au/altdns)

altdns generates permutations of words with domains, giving us more prospective hosts to check

* `altdns -i found_domains.txt -w wordlist.txt -o generated_list.txt`

If using with Gobuster, you might like to strip the domain from the suffix  
`sed -i s/[DOMAIN]$//g generated_list.txt`

## [Sublist3r](https://github.com/aboul3la/Sublist3r)

Sublist3r uses [https://github.com/TheRook/subbrute] behind the scenes to perform passive reconnaissance of domains

* `python3 sublist3r.py -d [DOMAIN] -b -v`

## [Amass](https://github.com/OWASP/Amass/)

Amass is another tool which can perform passive (and also active) recon

* `./amass enum -d [DOMAIN] -brute`

## Other

`dig`, `dnsrecon`, [DNSdumpster](https://dnsdumpster.com)


---

* Lecture Slides - COMP6443{I_FOUND_IT_5f6aecc4af7ad6b6df282a285523245e}
* Website
  * -QBSITE-/_static/scripts/devsite-dev.js
    * COMP6443{I_FOUND_IT_c9876289e54620cdfa7b4dc5bb66f1f3}
  * -QBSITE-/easfs-admin-backup
    * wow-how-did-i-find-this-super-secret-backup.-QBSITE- - COMP6443{I_FOUND_IT_3dab7a2b34c290abde68408b70950f68.ejUyMDY2Nzc=.WXpmZvKdB2LorrFpWJW0rw==}
  * Console Log
    * foobar-recruit.-QBSITE- - COMP6443{I_FOUND_IT_e45851b73586689a3d1a97be02d040a1.ejUyMDY2Nzc=./aCjgiaEWkdU1ThIOE+DQA==}
* DMARC Record
  * mailauth-prod.-QBSITE- - COMP6443{I_FOUND_IT_d5c28e68eda81cfc26951526ce849714.ejUyMDY2Nzc=.aAnctCt4PabCdTDiEd+s1A==}
* Dictionary
  * blog.-QBSITE- - COMP6443{I_FOUND_IT_126ac9f6149081eb0e97c2e939eaad52.ejUyMDY2Nzc=.A8ZA1vadvAxanMRz8w6bIA==}
  * test.-QBSITE- - COMP6443{I_FOUND_IT_098f6bcd4621d373cade4e832627b4f6.ejUyMDY2Nzc=.f0sdINk/9kTgRzuCcKWEUg==}
  * super-secret.admin.-QBSITE- - COMP6443{I_FOUND_IT_e7e964218749ecb479cdf80a7aade0a1.ejUyMDY2Nzc=.meIWBsxqw1ScmGEOyUBrqA==}
  * m.staging.-QBSITE- - COMP6443{I_FOUND_IT_c41a76367bce74581a13ab5eeda16514.ejUyMDY2Nzc=.xOcEF5obRakufC3En4+wDQ==}
  * m.-QBSITE- - COMP6443{I_FOUND_IT_6f8f57715090da2632453988d9a1501b.ejUyMDY2Nzc=.xc4tk7izI049tPDhGQ0RaA==}
  * mobile.-QBSITE- - COMP6443{I_FOUND_IT_532c28d5412dd75bf975fb951c740a30.ejUyMDY2Nzc=.31nY+KRGMzN6whS13OUfbQ==}
  * dev.-QBSITE- - COMP6443{I_FOUND_IT_e77989ed21758e78331b20e477fc5582.ejUyMDY2Nzc=.NL/5jT1qGrVUXFQOwGEBmA==}
  * adserver.-QBSITE- - COMP6443{I_FOUND_IT_e9c66fe2b4f79af58145cdd272b66e5a.ejUyMDY2Nzc=.tKYHBNecOKiq1yy5ngO3Ww==}
  * www-cdn.-QBSITE- - COMP6443{I_FOUND_IT_ccf538aec05bf0ea7313ec1698626103.ejUyMDY2Nzc=.TEDSKKQ1hPOhUGBpFbMe4g==}
  * www-preprod.-QBSITE- - COMP6443{I_FOUND_IT_927bb7e150b240f539875df667cb6c9b.ejUyMDY2Nzc=.q/jjh6+fWhyjajK3R4ov8A==}
  * www-dev.-QBSITE- - COMP6443{I_FOUND_IT_785b4b718c9e07edc8d53cb0e0f21de0.ejUyMDY2Nzc=.u9/g65W0iQUycBO7OR3OBQ==}
  * www-staging.-QBSITE- - COMP6443{I_FOUND_IT_fe955dc11265ad268ddafb2a5a1a82e2.ejUyMDY2Nzc=.Rifzxn41gETZnQrXEWQUbQ==}
  * careers.-QBSITE- - COMP6443{I_FOUND_IT_adf78c4508138a91472dcc053ab8eed4.ejUyMDY2Nzc=.4veknEPPTbjUumj4wILzWA==}
  * banking.-QBSITE- - COMP6443{I_FOUND_IT_6351e4efddc359eca697894df2bfd02d.ejUyMDY2Nzc=.z7+Hcw0Zh4pPqg8kdU9CAQ==}
  * creditcard.-QBSITE- - COMP6443{I_FOUND_IT_3c92742f3c1349e9c46fe4dd5da62a98.ejUyMDY2Nzc=.gkrho81JZY5/CiX/VHa0iA==}
  * vault42.-QBSITE- - COMP6443{I_FOUND_IT_f52da30d6fb4885ed885a978a8c2ae78.ejUyMDY2Nzc=.Z7Xi0DqoWKB/pRa2pFlZww==}
  * vault42.sandbox.-QBSITE- - COMP6443{I_FOUND_IT_a731277dbd3f90542e07d5eb065d3780.ejUyMDY2Nzc=.iWt8cP4ICsyzh9yI3RoGNA==}
  * dev-eu1.-QBSITE- - COMP6443{I_FOUND_IT_d3346fb4fc9bb23e6f859d7caaceac42.ejUyMDY2Nzc=.zyc2mpGJwTrEWj3UtP+QWA==}
  * www-cdn-au.-QBSITE- - COMP6443{I_FOUND_IT_86aa326b207fa9ac971558f6f17284aa.ejUyMDY2Nzc=.VF/uABJatqLVKrsZiLtUhw==}
  * www-cdn-us.-QBSITE- - COMP6443{I_FOUND_IT_5778ddae213588c275587da915c228e6.ejUyMDY2Nzc=.EmlJUB2Ci4WGJYTyC7Qgow==}
  * www-cdn-hk.-QBSITE- - COMP6443{I_FOUND_IT_9fc3ff6590918446a112507926789ea4.ejUyMDY2Nzc=.wwOyP5CEZx3OegceCp/cxQ==}
  * staging-na1.-QBSITE- - COMP6443{I_FOUND_IT_a0c86aed7be079ea1169b1073163dbcb.ejUyMDY2Nzc=.Q9fm8iLTQNUZL3S3//xg1g==}
  * staging-na2.-QBSITE- - COMP6443{I_FOUND_IT_b353873786888022691f267564b2dd9d.ejUyMDY2Nzc=.mLspeqOVJLtGTe1nAe8Knw==}