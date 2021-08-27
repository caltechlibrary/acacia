<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
    <link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="/acacia/css/site.css">
</head>
<body>
<header>
<span id="library_logo"><a href="http://library.caltech.edu" title="link to Caltech Library Homepage"><img src="/acacia/assets/liblogo.gif" alt="Caltech Library logo"></a></span>
<span id="project_logo"><img src="/acacia/assets/acacia-icon.svg" alt="Acacia project logo"></span>
</header>
<nav>
<% include('nav.tpl') %>
</nav>

<section>
% if form == 'add-doi':
%    include('add-doi.tpl')
% elif form == 'doi-submitted':
%    include('doi-submitted.tpl')
% else:
Not sure how to do that.
% end
</section>

<footer>
<span>&copy; 2021 <a href="https://www.library.caltech.edu/copyright">Caltech Library</a></span>
<address>1200 E California Blvd, Mail Code 1-32, Pasadena, CA 91125-3200</address>
<span><a href="mailto:library@caltech.edu">Email Us</a></span> 
<span>Phone: <a href="tel:+1-626-395-3405">(626)395-3405</a></span>
</footer>
</body>
</html>
