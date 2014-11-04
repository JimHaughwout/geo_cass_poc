from cassandra.cluster import Cluster
from  time_utils import *
from time_uuid import TimeUUID

#import uuid, time_uuid, datetime, time

KEY_SPACE = 'test'

'''
CREATE TABLE loc_hist (
  thing text,
  ts_id timeuuid,
  lat float,
  lng float,
  PRIMARY KEY (thing, ts_id))
WITH CLUSTERING ORDER BY (ts_id DESC);

INSERT INTO loc_hist (thing, ts_id, lat, lng) VALUES ('foo', now(), 38.2, -77.5);

CREATE TABLE loc_last (
  thing text,
  ts timestamp,
  lat float,
  lng float,
  temp float,
  PRIMARY KEY (thing));

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


'''
# Connect to C*
cluster = Cluster()
session = cluster.connect(KEY_SPACE)

# Prepare statements
get_loc_stmt = session.prepare("SELECT * FROM loc_hist")

locations = session.execute(get_loc_stmt)
for location in locations:
    print location.thing
    print location.ts_id
    print get_ts_for_timeuuid(location.ts_id, cassandra=True)


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