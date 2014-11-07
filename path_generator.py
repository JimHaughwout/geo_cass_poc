import settings
from map_utils import gen_path
from cassandra.cluster import Cluster
import sys 

# Create derived variables
if len(sys.argv) == 2:
    org = str(settings.ORG)
    thing = str(sys.argv[1])
else:
    print "Usage: %s thing_id" % sys.argv[0]
    sys.exit()

# Connect to Cassandra
cluster = Cluster()
session = cluster.connect(settings.KEY_SPACE)

# Generate prepared statements against following schema
'''
Queries the following schema:

CREATE TABLE loc_hist (
  org text,
  thing text,
  ts_id timeuuid,
  lat float,
  lng float,
  PRIMARY KEY ((org, thing), ts_id))
WITH CLUSTERING ORDER BY (ts_id DESC);
'''
get_loc_history = session.prepare("SELECT thing, dateOf(ts_id), lat, lng FROM loc_hist WHERE org=? AND thing=? LIMIT 5000")

# Query Cassandra for the dashboard
try:
    thing_locations = session.execute(get_loc_history, [org, thing])
except:
    raise

# Close Cassandra session
session.shutdown()

#Trigger the map
gen_path(thing_locations)



