from cassandra.cluster import Cluster
from  time_utils import *
from time_uuid import TimeUUID
import settings

#import uuid, time_uuid, datetime, time

'''
CREATE TABLE loc_hist (
  org text,
  thing text,
  ts_id timeuuid,
  lat float,
  lng float,
  PRIMARY KEY (org, thing, ts_id))
WITH CLUSTERING ORDER BY (thing ASC, ts_id DESC);

INSERT INTO loc_hist (org, thing, ts_id, lat, lng) VALUES ('foo', now(), 38.2, -77.5);

CREATE TABLE loc_last (
  thing text,
  ts timestamp,
  lat float,
  lng float,
  temp float,
  PRIMARY KEY (thing));

'''

def initialize_cassandra():
  cluster = Cluster()
  session = cluster.connect(settings.KEY_SPACE)
  return session

def initialize_dashboard(session):
  cql = "SELECT * FROM loc_hist WHERE org=? LIMIT ?"
  read_all_for_org = session.prepare(cql)
  return read_all_for_org

def initialize_logger(session):
  cql = "INSERT INTO loc_hist (org, thing, ts_id, lat, lng) VALUES (?, ?, ?, ?, ?)"
  insert_location = session.prepare(cql)
  return insert_location_read



def get_loc(session, cql_statement, org, limit=10000):
  locations = session.execute(cql_statement, [org, limit])
  for location in locations:
    for item in location:
      print item,
    print 


  
session = initialize_cassandra()
get_loc_stmt = initialize_dashboard(session)
get_loc(session, get_loc_stmt, 'sgs')



'''
def show_loc_hist(thing):
  cluster = Cluster()
  session = cluster.connect(KEY_SPACE)
  get_loc_stmt = session.prepare("SELECT * FROM loc_hist")
  locations = session.execute(get_loc_stmt)
  for location in locations:
    print location.thing
    print location.ts_id
    print get_ts_for_timeuuid(location.ts_id, cassandra=True)


show_loc_hist('foo')


# Connect to C*
cluster = Cluster()
session = cluster.connect(KEY_SPACE)

# Prepare statements
get_loc_stmt = session.prepare("SELECT * FROM loc_hist WHERE org=? AND ")



# Prepare statements
log_loc_stmt = session.prepare("INSERT INTO loc_hist (thing, ts, lat, lng) VALUES (?, dateOf(now()), ?, ?)")
upd_loc_stmt = session.prepare("INSERT INTO loc_last (thing, ts, lat, lng) VALUES (?, dateOf(now()), ?, ?)")
get_thing_loc_stmt = session.prepare("SELECT * FROM loc_hist WHERE thing=? LIMIT ?")
get_curr_loc_stmt = session.prepare("SELECT * FROM loc_last WHERE thing=?")



for i in xrange(0, ITER):
    print i
    time.sleep(DELTA_T)
    lat += (0.2 * delta_s)
    lng -= (0.8 * delta_s)
    session.execute(log_loc_stmt, [THING_ID, lat, lng])
    session.execute(upd_loc_stmt, [THING_ID, lat, lng])



locations = session.execute(get_thing_loc_stmt, [THING_ID, ITER])
print "\nLocation History - Last %d Reads:" % ITER
for loc in locations:
    print "%s is at (%.4f, %.4f) at %s" % \
     (loc.thing, loc.lat, loc.lng, loc.ts.isoformat())

cur = session.execute(get_curr_loc_stmt, [THING_ID])
print "\nMost Recently %s was last at (%.4f, %.4f) at %s" % \
 (cur[0].thing, cur[0].lat, cur[0].lng, cur[0].ts.isoformat())
'''