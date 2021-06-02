<!DOCTYPE html>
<html lang="en">
%include('common/banner.html')
  <head>
    <title>DOI: {{item.doi}}</title>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
    <meta http-equiv="Pragma" content="no-cache"/>
    <meta http-equiv="Expires" content="0"/>
%include('common/standard-inclusions.tpl')
  </head>
  <body>
    <header>
%include('common/header.tpl')
    </header>
    <nav>
%include('common/nav.tpl')
    </nav>
    <section>
FIXME: Display DOI metadata available or status if not.
    </section>
    <footer>
%include('common/footer.tpl')
    </footer>
  </body>
</html>
