<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
    <link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="/css/site.css">
</head>
<body>
<header>
<a href="http://library.caltech.edu" title="link to Caltech Library Homepage"><img src="/assets/liblogo.gif" alt="Caltech Library logo"></a>
</header>
<nav>
<% include('nav.tpl') %>
</nav>

<section>
<h1>DOI Report</h1>
<p>{{description}}</p>
<table>
<tr>
    <th>From</th>
    <th>Status</th>
    <th>DOI</th>
    <th>URL to object</th>
    <th>EPrint ID</th>
    <th>Export name</th>
</tr>
% for item in items: 
<tr>
   <td>{{item.m_from}}</td>
   <td>{{item.status}}</td>
   <td><a href="https://doi.org/{{item.doi}}">{{item.doi}}</a></td>
   <td><a href="{{item.object_url}}">
% if len(item.object_url) > 60:
{{item.object_url.replace('https://', '')[0:60]}} ...
% else:
{{item.object_url.replace('https://', '')}}
% end
</a></td>
<td>
% if item.eprint_id != None:
<a href="https://authors.library.caltech.edu/{{item.eprint_id}}">{{item.eprint_id}}</a>
% else:
None Available
% end
</td>
<td>{{item.bundle_name}}</td>
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
