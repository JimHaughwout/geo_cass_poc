import webbrowser
import os
from time_utils import get_ts_for_timeuuid
from models import Loc_Read

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
    file_name = 'location_dashboard.html'
    f = open(file_name, 'w')
    f.write("%s" % header)
    for location in locations:
      f.write("\n              [%.4f, %.4f, 'Thing %s at (%.3f, %.3f) as of %s']," % \
         (location.lat, location.lng, location.thing, 
          location.lat, location.lng, location.ts.isoformat()))
    f.write("%s" % footer)
    f.close()

    full_path = os.path.realpath(file_name)
    url = 'file://' + full_path
    webbrowser.open(url)
    #webbrowser.open_new_tab(url)
    print "Showing %d things." % len(locations)


def gen_path(location_path):
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
    file_name = 'location_path.html'
    f = open(file_name, 'w')
    f.write("%s" % header)
    for location in location_path:
      f.write("\n              [%.4f, %.4f, 'Thing %s at (%.3f, %.3f) as of %s']," % \
         (location.lat, location.lng, location.thing, 
          location.lat, location.lng, location.dateOf_ts_id.isoformat()))
    f.write("%s" % footer)
    f.close()

    full_path = os.path.realpath(file_name)
    url = 'file://' + full_path
    webbrowser.open(url)
    #webbrowser.open_new_tab(url)
    print "Showing %d locations for Thing %s." % (len(locations), location[0].thing)