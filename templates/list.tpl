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
<p>
<!-- 
<button><a href="{{base_url}}/get-messages">Get Messages</a></button>
<button><a href="{{base_url}}/messages-to-doi">Parse Messages</a></button>
<button><a href="{{base_url}}/retrieve-metadata">Retrieve Metadata</a></button>
-->
</p>
<h1>Manage DOI</h1>
<p>{{description}}</p>
<table>
<tr>
    <th class="action">&nbsp;</th>
    <th>Recieved</th>
    <th>From</th>
    <th>Status</th>
    <th>Metadata Retrieved</th>
    <th>EPrint ID</th>
    <th>DOI</th>
    <th>URL to PDF</th>
    <th>View XML</th>
    <th class="action">&nbsp;</th>
    <th class="action">&nbsp;</th>
</tr>
% for item in items: 
<tr>
   <td>
   % if item.eprint_id:
   &nbsp;
   % elif item.status == "ready":
   <button><a href="{{base_url}}/doi-reset/{{item.id}}" title="Clear the retrieved metadata for record {{item.id}} in Acacia">clear</a></button>
   % else:
   <button><a href="{{base_url}}/retrieve-metadata/{{item.id}}" title="retrieve the metadata via CrossRef or DataCite">look up</a></button>
   % end
   </td>
   <td>
   {{item.created.strftime("%Y-%m-%d")}}
   </td>
   <td>
% if ("<" in item.m_from) and (item.m_from.split('<', 2)[0] != ""):
   {{item.m_from.split('<', 2)[0].replace('"', '')}}
% else:
   {{item.m_from}}
% end
   </td>
   <td>
% if item.status == "ready":   
metadata retrieved   
% elif item.status == "pending":
   waiting for lookup
% elif item.eprint_id:
   in repository
% else:
   {{item.status}}
% end
   </td>
   <td>
% if item.status == "ready":
   {{item.updated.strftime("%Y-%m-%d")}}
% end
   </td>
   <td>
% if (item.eprint_id != None) and (item.eprint_id != 0):
<a href="{{view_url}}{{item.eprint_id}}" target="_blank">{{item.eprint_id}}</a>
% else:
   &nbsp;
% end
   </td>
   <td>
       <a href="https://doi.org/{{item.doi}}" target="_blank">{{item.doi}}</a>
   </td>
   <td><a href="{{item.object_url}}" target="_blank">
% if len(item.object_url) > 0:
{{item.object_url.replace('http://', '').replace('https://', '').split(sep="/", maxsplit=2)[0]}}
% end
</a></td>
   <td>
% if (item.status == "ready"):
   <a href="{{base_url}}/eprint-xml/{{item.id}}" target="_blank">XML</a>
% end
   </td>
   <td>
% if item.status == "ready" and not item.eprint_id:
       <button><a href="{{base_url}}/item-import/{{item.id}}" title="Import item into EPrints">Import</a></button>
% end
   </td>
   <td>
% if item.status == "imported" or item.eprint_id:
       <button><a href="{{base_url}}/doi-remove/{{item.id}}" title="Complete by removing item from Acacia">Completed</a></button>

% else:
       <button><a href="{{base_url}}/doi-remove/{{item.id}}" title="Remove item from Acacia">Remove</a></button>
% end
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
