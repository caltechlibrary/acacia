<!DOCTYPE html>
<html lang="en">
  %include('common/banner.html')
  <head>
    %include('common/standard-inclusions.tpl')
    <title>Welcome to Caltech Acacia</title>
  </head>
  
  <body>
    <header>
%include('common/header.tpl')
    </header>
    <nav>
%include('common/nav.tpl')
    </nav>
    <section>

      <h1>Welcome to Caltech Acacia</h1>

      <h2>The Caltech <strong>A</strong>utomated Caltech<strong>A</strong>UTHORS <strong>C</strong>atalog <strong>I</strong>ngest <strong>A</strong>gent</h2>
      <p><strong>Caltech Acacia</strong> implements content submission to CaltechAUTHORS via DOI metadata retrieval.</p>
        
      <form method="POST" action="{{base_url}}/login">

            %if get('login_failed', False):
            <div classs="form-group">
              <span class="error text-danger">Ooops! Incorrect user or password. Try again?</span>
            </div>
            %end

            <div>
              <label>Acacia user</label>
              <input name="email" type="text" autocomplete="off" placeholder="User" required autofocus/>
            </div>

            <div>
              <label>Acacia password</label>
              <input name="password" type="text" autocomplete="off"
                     placeholder="Password" required/>
            </div>

            <input value="Login" type="submit" />
          </form>

    </section>
    <footer>
%include('common/footer.tpl')
    </footer>
  </body>
</html>
