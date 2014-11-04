import webbrowser
import os

FILE_NAME = 'foo.html'

data = """
          [37.4232, -122.0853, 'Work'],
          [37.4289, -122.1697, 'University'],
          [37.6153, -122.3900, 'Airport'],
          [37.4422, -122.1731, 'Shopping']"""

def gen_map(data, file_name):
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

    footer = """
            ]);
    
            var map = new google.visualization.Map(document.getElementById('map_div'));
            map.draw(data, {showTip: true});
          }

        </script>
      </head>

      <body>
        <div id="map_div" style="width: 1280px; height: 800px"></div>
      </body>
    </html>
    """

    f = open(file_name, 'w')
    f.write("%s%s%s" % (header, data, footer))
    f.close()

    full_path = os.path.realpath(file_name)
    url = 'file://' + full_path
    webbrowser.open_new_tab(url)

gen_map(data, FILE_NAME)
