Add a DOI
=========

This form accepts a DOI and a URL (optional) to the digital object
which can be be used to generate EPrint XML for import into
[CaltechAUTHORS](https://authors.library.caltech.edu).

<form method="post" action="/add-doi">
<input type="hidden" name="uname" value="{{uname}}">
<div>
<label>DOI</label> <input type="text" name="doi" value="" title="Enter a DOI here"></div>

<label>URL to Object</label> <input type="text" name="object_url" value="" title="Enter the URL for the digital object"></div>
</div>
<p>
<input type="submit" name="submit" value="Add record">
</p>
</form>