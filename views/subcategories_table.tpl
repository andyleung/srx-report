<!DOCTYPE html>

<html>
  <head>
    <title>Subcategories App Report</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
      th {background: lightblue; border-color: black; text-align: left;}
    </style>
  </head>

<h2>Application by Subcategories</h2>
<body>
<!-- button for session sorting -->
<table>
  <tr>
    <td>
      <form action="/ag_report_apps">
          <input type="submit" value="Main">
      </form>
    </td>
  </tr>
</table>

%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<table border="1">
  <tr>
    <th>Applications</th><th>Counts</th><th>Bytes</th><th>Sessions</th>
  </tr>
%for row in rows:
  <tr>
<!--   %for col in row: -->
    <th>{{row[0]}}</th><td>{{row[1]}}</td><td>{{row[2]}}</td><td>{{row[3]}}</td>
  %end
  </tr>
%end
</table>

</body>
</html>
