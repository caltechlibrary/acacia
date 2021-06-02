<!DOCTYPE html>
<html lang="en">
%include('common/banner.html')
  <head>
    <title>Add or edit a DOI retrieval request</title>
%include('common/standard-inclusions.tpl')
  </head>
  <body>
    <header><!-- page header, not to be confused with a section header -->
%include('common/header.tpl')
%include('common/nav.tpl')
    </header>
    <section>

        <h2>
          %if item:
          Edit DOI {{item.doi}}
          %else:
          Add new DOI
          %end
        </h2>

        <p>FIXME: instructions/descriptoin goes here</p>
        <form method="POST" action="{{base_url}}/update/{{action}}">

          <label for="doi">
            <span>DOI</span>
            <input name="doi" type="input"
                   placeholder="DOI - digital object identifier"
                   %if item.doi:
                   value="{{item.doi}}"
                   %end
                   required autofocus>
          </label>

          <label for="pdf">
            <span>PDF URL</span>
            <input name="doi" type="input"
                   placeholder="URL to retrieve PDF"
                   %if item.pdf:
                   value="{{item.pdf}}"
                   %end
                   required autofocus>
          </label>

          <div>
              <input name="cancel" value="Cancel" type="submit" formnovalidate/>
              <input id="btnAdd" type="submit"
                     name="add"
                     %if item:
                     value="Save"
                     %else:
                     value="Add"
                     %end
                     />
          </div>
        </form>
      </div>
    </section>
    <footer><!-- page footer, not to be confused with a section footer -->
%include('common/footer.tpl')
    </footer>
  </body>
</html>
