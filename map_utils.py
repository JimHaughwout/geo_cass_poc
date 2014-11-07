import webbrowser
import os
from time_utils import get_ts_for_timeuuid
from models import Loc_Read

def gen_map(locations):
  '''
  Generates HTML and JS for a 'simple markers' Google map and displays 
  latest location of things in a browser.

  :param locations: list of location reads (see models.Loc_Read)
  :returns Prints count of markers displayed and call browser to display map
  
  '''
    # HTML/JS Header
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
    # HTML/JS Footer
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
    # Create the file
    file_name = 'location_dashboard.html'
    f = open(file_name, 'w')
    f.write("%s" % header)
    for location in locations:
      f.write("\n              [%.4f, %.4f, 'Thing %s at (%.3f, %.3f) as of %s']," % \
         (location.lat, location.lng, location.thing, 
          location.lat, location.lng, location.ts.isoformat()))
    f.write("%s" % footer)
    f.close()

    # Display the file in a browser and print results
    full_path = os.path.realpath(file_name)
    url = 'file://' + full_path
    webbrowser.open(url)
    print "Showing %d things." % len(locations)


def gen_path(location_path):
  '''
  Generates HTML and JS for a 'simple markers' Google map and displays
  path of a thing in a browser.

  :param locations: list of location reads (see models.Loc_Read)
  :returns Prints count of markers displayed and call browser to display map
  
  '''
    # HTML/JS Header
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

    # HTML/JS Footer
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
    
    # Generate the file
    file_name = 'location_path.html'
    f = open(file_name, 'w')
    f.write("%s" % header)
    for location in location_path:
      f.write("\n              [%.4f, %.4f, 'Thing %s at (%.3f, %.3f) as of %s']," % \
         (location.lat, location.lng, location.thing, 
          location.lat, location.lng, location.dateOf_ts_id.isoformat()))
    f.write("%s" % footer)
    f.close()

    # Display in a browser, print the path length
    full_path = os.path.realpath(file_name)
    url = 'file://' + full_path
    webbrowser.open(url)
    print "Showing %d locations for Thing %s." % (len(location_path), location_path[0].thing)