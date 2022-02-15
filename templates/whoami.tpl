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
<span id="library_logo"><a href="https://library.caltech.edu" title="link to Caltech Library Homepage"><img src="{{base_url}}/assets/liblogo.gif" alt="Caltech Library logo"></a></span>
<span id="project_logo"><img src="{{base_url}}/assets/acacia-icon.svg" alt="Acacia project logo"></span>
</header>
<nav>
<% include('nav.tpl') %>
<% include("user_info.tpl") %>
</nav>

<section>
<h1>Who am I?</h1>
<p>{{description}}</p>
<table>
    <tr><th>userid</th><td>{{person.userid}}</td></tr>
    <tr><th>uname</th><td>{{person.uname}}</td></tr>
    <tr><th>name</th><td>{{person.name.honourific}} {{person.name.given}} {{person.name.family}} {{person.name.lineage}}</td></tr>
    <tr><th>display name</td><td>{{person.display_name}}</td></tr>
% if not person.hide_email:
    <tr><th>email</th><td>{{person.email}}</td></tr>
% end
    <tr><th>role</th><td>{{person.role}}</td></tr>
    <tr><th>created</th><td>{{person.created}}</td></tr>
% if shib_user:
    <tr><th>REMOTE_USER</th><td>{{shib_user}}</td></tr>
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
