<!DOCTYPE html>
<html>
<head>
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
</nav>

<section>
<p>
<!-- 
<button><a href="{{base_url}}/get-messages">Get Messages</a></button>
<button><a href="{{base_url}}/messages-to-doi">Parse Messages</a></button>
<button><a href="{{base_url}}/retrieve-metadata">Retrieve Metadata</a></button>
-->
</p>
<h1>DOI Report</h1>
<p>{{description}}</p>
<table>
<tr>
    <th class="action">&nbsp;</th>
    <th>From</th>
    <th>Status</th>
    <th>DOI</th>
    <th>URL to PDF</th>
    <th>Export</th>
    <th class="action">&nbsp;</th>
</tr>
% for item in items: 
<tr>
   <td>
   % if item.status == "ready":
   <button><a href="{{base_url}}/doi-reset/{{item.id}}" title="Clear the retrieved metadata from record">reset</a></button>
   % else:
   <button><a href="{{base_url}}/retrieve-metadata/{{item.id}}" title="retrieve the metadata via CrossRef or DataCite">Get DOI</a></button>
   % end
   </td>
   <td>
% if ("<" in item.m_from) and (item.m_from.split('<', 2)[0] != ""):
   {{item.m_from.split('<', 2)[0]}}
% else:
   {{item.m_from}}
% end
   </td>
   <td>
% if item.status == "ready":
   % if item.eprint_id == None:
    {{item.status}}
   % else:
<a href="https://authors.library.caltech.edu/{{item.eprint_id}}" target="_blank">EPrint {{item.eprint_id}}</a>
   % end
% elif item.status == "unprocessed":
    pending
% else:
   {{item.status}}
% end
   </td>
   <td>
       <a href="https://doi.org/{{item.doi}}" target="_blank">{{item.doi}}</a>
   </td>
   <td><a href="{{item.object_url}}">
% if len(item.object_url) > 0:
{{item.object_url.replace('http://', '').replace('https://', '').split(sep="/", maxsplit=2)[0]}}
% end
</a></td>
   <td>
% if item.status == "ready":
   <a href="{{base_url}}/eprint-xml/{{item.id}}" target="_blank">EPrint XML</a>
% end
   </td>
   <td>
       <button><a href="{{base_url}}/doi-remove/{{item.id}}">Remove</a></button>
   </td>
</tr>
% end
</table>
</section>

<footer>
<span>&copy; 2021 <a href="https://www.library.caltech.edu/copyright">Caltech Library</a></span>
<address>1200 E California Blvd, Mail Code 1-32, Pasadena, CA 91125-3200</address>
<span><a href="mailto:library@caltech.edu">Email Us</a></span> 
<span>Phone: <a href="tel:+1-626-395-3405">(626)395-3405</a></span>
</footer>
</body>
</html>
