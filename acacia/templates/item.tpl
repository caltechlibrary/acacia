<!DOCTYPE html>
<html>
<head>
    <title>${title}</title>
    <link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="/static/css/site.css">
</head>
<body>
<header>
<a href="http://library.caltech.edu" title="link to Caltech Library Homepage"><img src="/static/assets/liblogo.gif" alt="Caltech Library logo"></a>
</header>
<nav>
${if(nav)}${nav}${endif}
</nav>

<section>
${body}
</section>

<footer>
<span>&copy; 2020 <a href="https://www.library.caltech.edu/copyright">Caltech Library</a></span>
<address>1200 E California Blvd, Mail Code 1-32, Pasadena, CA 91125-3200</address>
<span><a href="mailto:library@caltech.edu">Email Us</a></span> 
<span>Phone: <a href="tel:+1-626-395-3405">(626)395-3405</a></span>
</footer>
</body>
</html>
