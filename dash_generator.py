import settings
from map_utils import gen_map
from cassandra.cluster import Cluster

# Connect to Cassandra
cluster = Cluster()
session = cluster.connect(settings.KEY_SPACE)

# Generate prepared statements
'''
Requires the following schema

CREATE TABLE loc_dash (
  org text,
  thing text,
  ts timestamp,
  lat float,
  lng float,
  PRIMARY KEY (org, thing))
WITH CLUSTERING ORDER BY (thing ASC);

'''


# Limit to 10K results. We could override but this is likely already too much.
get_loc_dash = session.prepare("SELECT * FROM loc_dash WHERE org=? LIMIT 5000")

# Query Cassandra for the dashboard
try:
    things = session.execute(get_loc_dash, [str(settings.ORG)])
except:
    raise
# Close Cassandra session
session.shutdown()

#Trigger the map
gen_map(things)



