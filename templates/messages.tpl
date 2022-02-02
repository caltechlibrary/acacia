<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{title}}</title>
    <link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="{{base_url}}/css/site.css">
</head>
<body>
<header>
<span id="library_logo"><a href="http://library.caltech.edu" title="link to Caltech Library Homepage"><img src="{{base_url}}/assets/liblogo.gif" alt="Caltech Library logo"></a></span>
<span id="project_logo"><img src="{{base_url}}/assets/acacia-icon.svg" alt="Acacia project logo"></span>
</header>
<nav>
<% include('nav.tpl') %>
<% include('user_info.tpl') %>
</nav>

<section>
<p>
<!-- <button><a href="{{base_url}}/get-messages">Get Messages</a></button><! -->
<button><a href="{{base_url}}/messages-to-doi">Process Messages</a></button>
<!--
<button><a href="{{base_url}}/retrieve-metadata">Retrieve Metadata</a></button>
-->
</p>
<h1>Message Report</h1>
<p>{{description}}</p>
<table>
<thead>
<tr>
    <th class="action">Reset</th>
    <th class="from">From</th>
    <th class="status">Status</th>
    <th class="subject">Subject</th>
    <th class="datestamp">Date</th>
    <th class="action">Remove</th>
</tr>
</thead>
<tbody>
% for item in items:
   <tr>
   <td class="action">
   % if item.m_processed:
   <button><a href="{{base_url}}/message-reset/{{item.id}}">reset</a></button>
   % end
   </td>
   <td class="from">
    % if len(item.m_from) > 0:
        {{item.m_from.split('<', 2)[0]}}
    % end
   </td>
   <td class="status">
% if item.m_processed: 
processed
% else:
unprocessed
% end
   </td>
   <td class="subject">{{item.m_subject}}</td>
   <td class="datestamp">
   {{item.m_date.strftime("%Y-%m-%d")}}
   </td>
   <td class="action">
   <button><a href="{{base_url}}/message-remove/{{item.id}}">Remove</a></button>
   </td>
   </tr>
% end
</tbody>
</table>
</section>

<footer>
<span>&copy; 2021 <a href="https://www.library.caltech.edu/copyright">Caltech Library</a></span>
<address>1200 E California Blvd, Mail Code 1-32, Pasadena, CA 91125-3200</address>
<span><a href="mailto:library@caltech.edu">Email Us</a></span> 
<span>Phone: <a href="tel:+1-626-395-3405">(626)395-3405</a></span>
</footer>
<script type="module" src="/widgets/sorttable.js"></script>
<script type="module">
"use strict";
import { make_table_sortable } from '/widgets/sorttable.js';
make_table_sortable('table');
</script>
</body>
</html>
