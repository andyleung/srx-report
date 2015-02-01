<!DOCTYPE html>

<html>
  <head>
    <title>Application Statistics</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
      th {background: lightblue; border-color: black; text-align: left;}
    </style>
  </head>

<h2>Application Statistics</h2>
<body>
<!-- button for session sorting -->
<table>
  <tr>
    <td>
      <form action="/ag_report_apps">
          <input type="submit" value="By Apps">
      </form>
    </td>
    <td>
      <form action="/ag_report_sessions">
          <input type="submit" value="By Sessions">
      </form>
    </td>
    <td>   
       <form action="/ag_report_kbytes">
           <input type="submit" value="By Kbytes">
       </form>
    </td>
  </tr>
</table>

%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<table border="1">
  <tr>
    <th>Applications</th><th>Sessions</th><th>KBytes</th><th>Risk</th><th>Categories</th><th>Subcategories</th>
  </tr>
%for row in rows:
  <tr>
<!--   %for col in row: -->
    <th>{{row[0]}}</th><td>{{row[1]}}</td><td>{{row[2]}}</td><td>{{row[3]}}</td><td>{{row[4]}}</td><td>{{row[5]}}</td>
  %end
  </tr>
%end
</table>

</body>
</html>
