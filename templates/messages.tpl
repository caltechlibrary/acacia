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
<h1>Message Report</h1>
<p>{{description}}</p>
<table>
<tr> <th>Date</th> <th>From</th> <th>Subject</th> <th>Processed?</th></tr>
% for item in items:
   <tr>
   <td>{{item.m_date[0:11]}}</td>
   <td>{{item.m_from}}</td>
   <td>{{item.m_subject}}</td>
   <td>
% if item.m_processed: 
✔️
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
