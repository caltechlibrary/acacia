---
title : About to Acacia
---

About Acacia
=================

Acacia is a micro service for processing [DOI](https://doi.org)
submission requests for
[CaltechAUTHORS](https://authors.library.caltech.edu). It is based on 
an Email submission of a DOI and a link to a PDF. Acacia allows you to
manage the incoming DOI submissions and generate EPrint XML that can
be used to generate EPrints records using EPrint XML import
functionality.

Developers
----------

(alphabetically)

+ R. S. Doiel
+ Mike Hucka
+ Tommy Keswick
+ Kathy Johnson
+ Tom Morrell
+ George Porter

<version-info id="version-info"></version-info>

<script type="module" src="widgets/version-info.js"></script>

<script type="module">
"use strict";
let version_info = document.getElementById('version-info');

function updateVersionInfo() {
    let src = this.responseText,
        obj = JSON.parse(src);
    version_info.value = obj;
}

function retrieveVersionInfo() {
    let oReq = new XMLHttpRequest();
    oReq.addEventListener('load', updateVersionInfo);
    oReq.open('GET', '/version');
    oReq.send();
}
retrieveVersionInfo();
</script>
