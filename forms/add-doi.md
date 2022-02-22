Add a DOI
=========

This form accepts a DOI and a URL (optional) to the digital object
which can be be used to generate EPrint XML for import into
[CaltechAUTHORS](https://authors.library.caltech.edu).

<form method="post" action="{{base_url}}/add-doi">
<input type="hidden" name="uname" value="{{uname}}">
<div class="input-pair">
<label>DOI</label>
<input type="text" name="doi" value="" title="Enter a DOI here">
</div>
<div class="input-pair">
<label>URL to PDF</label>
<input type="text" name="object_url" value="" title="Enter the URL for the PDF or other digital object">
</div>
<p>
<input type="submit" name="submit" value="Add record">
</p>
</form>
