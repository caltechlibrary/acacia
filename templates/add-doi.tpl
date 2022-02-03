<h1 id="add-a-doi">Add a DOI</h1>
<p>This form accepts a DOI and a URL (optional) to the digital object which can be be used to generate EPrint XML for import into <a href="https://authors.library.caltech.edu">CaltechAUTHORS</a>.</p>
<form method="post" action="{{base_url}}/add-doi">
<input type="hidden" name="uname" value="{{uname}}">
<div>
<p><label for="doi-entry">DOI</label> <input id="doi-entry" type="text" name="doi" value="" title="Enter a DOI here"></p>
</div>
<div>
<p><label for="url-to-pdf">URL to PDF</label> <input id="url-to-pdf" type="text" name="object_url" value="" title="Enter the URL for the PDF or other digital object"></p>
</div>
<p>
<input type="submit" name="submit" value="Add record">
</p>
</form>
