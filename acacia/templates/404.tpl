<!DOCTYPE html>
<html lang="en">
%include('common/banner.inc')
  <head>
    <title>Error</title>
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

      <div>
        <img src="{{base_url}}/static/missing.jpg"
             style="max-width: 500px" width="80%"
             title="Photo taken in the Sherman Fairchild Library in January, 2021. Copyright 2021 Rebecca Minarez. Distributed under a CC BY-NC-SA 4.0 license."
             alt="Photo of missing books by Rebecca Minjarez, Caltech.">

        <h4>Very sorry, but that seems to be missing &#8230;</h4>

        <p>We hate when that happens! Maybe it's been misplaced, or
        maybe it's really gone. Our staff will take note of the
        missing item. Our apologies for the inconvenience.</p>

        <p><small>(Code {{code}}: {{message}})</small></p>
      </div>

    </section>
    <footer>
%include('common/footer.tpl')
    </footer>
  </body>
</html>
