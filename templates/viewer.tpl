<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{title}}</title>
    <link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="{{base_url}}/css/site.css">
</head>
<body>
<header>
<span id="library_logo"><a href="http://library.caltech.edu" title="link to Caltech Library Homepage"><img src="{{base_url}}/assets/liblogo.gif" alt="Caltech Library logo"></a></span>
<span id="project_logo"><img src="{{base_url}}/assets/acacia-icon.svg" alt="Acacia project logo"></span>
</header>
<nav>
<% include('nav.tpl') %>
<% include('user_info.tpl') %>
</nav>

<section>
<h1>View Record (#{{rec_id}})</h1>
<p>{{description}}</p>

<record-viewer id="viewer"></record-viewer>

</section>

<footer>
<span>&copy; 2021 <a href="https://www.library.caltech.edu/copyright">Caltech Library</a></span>
<address>1200 E California Blvd, Mail Code 1-32, Pasadena, CA 91125-3200</address>
<span><a href="mailto:library@caltech.edu">Email Us</a></span> 
<span>Phone: <a href="tel:+1-626-395-3405">(626)395-3405</a></span>
</footer>
<script type="module" src="{{base_url}}/widgets/viewer.js"></script>
<script type="module">
"use strict";
import { RecordViewer } from '{{base_url}}/widgets/viewer.js';
let viewer_elem = document.getElementById('viewer'),
    rec_id = {{rec_id}};

function updateViewer() {
    let src = this.responseText,
    obj = JSON.parse(src);
    viewer_elem.value = obj;
}

function retrieveRecord(rec_id) {
    let oReq = new XMLHttpRequest();
    oReq.addEventListener('load', updateViewer);
    oReq.open('GET', `/viewer-json/${rec_id}`);
    oReq.send();
}
retrieveRecord(rec_id);
</script>
</body>
</html>