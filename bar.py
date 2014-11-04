s = """
This is a long
    text fragment.
How is this?
"""

header = """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["map"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Lat', 'Long', 'Name'],"""
data = """
          [37.4232, -122.0853, 'Work'],
          [37.4289, -122.1697, 'University'],
          [37.6153, -122.3900, 'Airport'],
          [37.4422, -122.1731, 'Shopping']"""
footer = """
        ]);

        var map = new google.visualization.Map(document.getElementById('map_div'));
        map.draw(data, {showTip: true});
      }

    </script>
  </head>

  <body>
    <div id="map_div" style="width: 1024px; height: 768px"></div>
  </body>
</html>
"""
print "%s%s%s" % (header,data,footer)

