import settings
#from datetime import datetime, timedelta
#from models import Loc_Read
from map_utils import gen_trail
from cassandra.cluster import Cluster
#from time_utils import make_timeuuid
for sys import argv

# Create derived variables
org = str(settings.ORG)
thing = str(argv[1])

# Connect to Cassandra
cluster = Cluster()
session = cluster.connect(settings.KEY_SPACE)

# Generate prepared statements
'''
CREATE TABLE loc_hist (
  org text,
  thing text,
  ts_id timeuuid,
  lat float,
  lng float,
  PRIMARY KEY ((org, thing), ts_id))
WITH CLUSTERING ORDER BY (ts_id DESC);
'''


# Limit to 10K results. We could override but this is likely already too much.
get_loc_history = session.prepare("SELECT * FROM loc_history WHERE org=? AND thing=? LIMIT 5000")

# Query Cassandra for the dashboard
try:
    thing_locations = session.execute(get_loc_history, [org, thing])
except:
    raise
# Close Cassandra session
session.shutdown()

#Trigger the map
gen_trail(thing_locations)



