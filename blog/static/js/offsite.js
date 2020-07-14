// Remove direct references to QB, and rely on client-side JS to reveal

(function () {
  const elems = document.evaluate("//text()[contains(., '-QBSITE-')]", document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null)
  if (!elems.snapshotLength) return

  // Remedial obfuscation so it doesn't show up on Google... hahahaha.... :/
  let replace = 'Vm1wR1UxSXlTWGhYV0d4V1ltczFiMVJVU2pSV2JHeHpXa2M1V2xadGVIcFdiVEZIVkd4YWRHVkdjRnBYU0VKSVdWVmtTMVp0U2tWV2JGWlhWbXRaZWxaVldrWlBWa0pTVUZRd1BRPT0='
  for (let i = 7; i--;) replace = atob(replace)
  const re = new RegExp('-QBSITE-', 'g')

  // String replace
  for (let i = 0; i < elems.snapshotLength; i++) {
    const elem = elems.snapshotItem(i)
    elem.data = elem.data.replace(re, replace)
  }
})()
