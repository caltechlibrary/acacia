<!DOCTYPE html>
<html lang="en">
%include('common/banner.html')
  <head>
    <title>Error</title>
%include('common/standard-inclusions.tpl')
  </head>
  <body>
    <header><!-- page header, not to be confused with section header -->
%include('common/header.tpl')
    </header>
    <nav>
%include('common/nav.tpl')
    </nav>
    <section>
      <h4 class="alert-heading">Error: {{summary}}</h4>
      <p id="error-message">{{message}}</p>
      </div>
    </section>
    <footer><!-- page footer, not to be confused with a section footer -->
%include('common/footer.tpl')
    </footer>
  </body>
</html>
