<ul class="navigation">
   <li><a href="{{base_url}}/manage">Manage</a></li>
   <li><a href="{{base_url}}/about">About</a></li>
   %if person == None:
   <li><a href="{{base_url}}/login">Login</a></li>
   %else:
   <li><a href="{{base_url}}/logout">Logout</a></li>
   %end
</ul>
