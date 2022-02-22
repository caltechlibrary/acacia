<h1 id="add-a-doi">Add a DOI</h1>
<<<<<<< HEAD
<p>This form accepts a DOI and a URL (optional) to the digital object which can be be used to generate EPrint XML for import into <a href="https://authors.library.caltech.edu">CaltechAUTHORS</a>.</p>
=======
<p>This form accepts a DOI and a URL (optional) to the digital object
which can be be used to generate EPrint XML for import into <a
href="https://authors.library.caltech.edu">CaltechAUTHORS</a>.</p>
>>>>>>> 92af7b09bce2d1e5e4bb14d16ab95dc4ea673bce
<form method="post" action="{{base_url}}/add-doi">
<input type="hidden" name="uname" value="{{uname}}">
<div>
<p><label>DOI</label> <input type="text" name="doi" value="" title="Enter a DOI here"></p>
</div>
<div>
<p><label>URL to PDF</label> <input type="text" name="object_url" value="" title="Enter the URL for the PDF or other digital object"></p>
</div>
<p>
<input type="submit" name="submit" value="Add record">
</p>
</form>
