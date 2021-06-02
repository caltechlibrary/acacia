<!DOCTYPE html>
<html lang="en">
%include('common/banner.inc')
  <head>
    <title>Caltech Acacia</title>
%include('common/standard-inclusions.tpl')
  </head>
  <body>
  <header><!-- page header, not be confused with a section header -->
%include('common/header.tpl')
  </header>
  <nav>
%include('common/nav.tpl')
  </nav>
  <section>
    <h1>Caltech Acacia</h1>

    <h2>The Caltech Library <strong>A</strong>utomated <strong>C</strong>altechAUTHORS <strong>C</strong>atalog <strong>I</strong>ngest <strong>Agent<strong></h2>

    <h3 class="version_number">Version {{__version__}}</h3>

    <p><strong>Caltech Acacia</strong> implements content submission to
    CaltechAUTHORS via DOI metadata retrieval.</p>

  </section>
  <footer><!-- page footer, not to be confused with a section footer -->
%include('common/footer.tpl')
  <footer>
  </body>
</html>
