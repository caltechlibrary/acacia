% if error_message:
<h1 id="doi-submitted">Submission rejected</h1>
<p>{{error_message}}</p>
<p><a href="/acacia/add-doi">Add anther DOI</a>.</p>
% else:
<h1 id="doi-submitted">DOI Submitted</h1>
<p>Thank you for submitting {{doi}}. You can view the process status in the <a href="/acacia/list/">DOI Report</a> or <a href="/acacia/add-doi">Add anther DOI</a>.</p>
% end

