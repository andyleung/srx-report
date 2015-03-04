<!DOCTYPE html>

<html>
  <head>
    <title>HTTP App Report</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
      th {background: lightblue; border-color: black; text-align: left;}
    </style>
    <script src="http://d3js.org/d3.v3.min.js"></script>
    <script src="http://dimplejs.org/dist/dimple.v2.1.2.min.js"></script>
  </head>

<h2>Application use HTTP or HTTPS ports</h2>


<!-- button for session sorting -->
<table>
  <tr>
    <td>
      <form action="/ag_graph_characteristic">
          <input type="submit" value="Main">
      </form>
    </td>
  </tr>
</table>
<body>
  <script type="text/javascript">
    var svg = dimple.newSvg("body", 800, 600);
    var data = rows
    var chart = new dimple.chart(svg, data);
    chart.addCategoryAxis("_id", "characteristic");
    chart.addMeasureAxis("count", "count");
    chart.addSeries(null, dimple.plot.bar);
    chart.draw();
  </script>
</body>

</html>