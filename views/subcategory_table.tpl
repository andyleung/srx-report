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
    <td>   
       <form action="/ag_report_risk">
           <input type="submit" value="By Risk">
       </form>
    </td>
  </tr>
</table>

%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<table border="1">
  <tr>
    <th>Subcategories</th><th>Application counts</th><th>Sessions</th><th>Bytes</th>
  </tr>
%for row in rows:
  <tr>
<!--   %for col in row: -->
    <th>{{row['_id']}}</th><td>{{row['app_count']}}</td><td>{{row['Sessions']}}</td><td>{{row['Bytes']}}</td>
  %end
  </tr>
%end
</table>

</body>
</html>
