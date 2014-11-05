import webbrowser
import os
from time_utils import get_ts_for_timeuuid

FILE_NAME = 'current_locations.html'

def gen_google_coords(locations):
    for location in thing_locations:
        print "          [%.4f, %.4f, 'Thing-%s @ %s']," % \
         (location.lat, location.lng, location.id, location.ts)


data = """
          [37.4232, -122.0853, 'Work'],
          [37.4289, -122.1697, 'University'],
          [37.6153, -122.3900, 'Airport'],
          [37.4422, -122.1731, 'Shopping']"""

def gen_map(locations):
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
    #TODO Switch to LocRead

    f = open(FILE_NAME, 'w')
    f.write("%s" % header)
    for location in locations:
      f.write("          [%.4f, %.4f, 'Thing-%s at (%.3f, %.3f) as of %s']," % \
         (location.lat, location.lng, 
          location.id, location.lat, location.lng, location.ts_id)
    f.write("%s" % footer)
    f.close()

    full_path = os.path.realpath(FILE_NAME)
    url = 'file://' + full_path
    webbrowser.open_new_tab(url)