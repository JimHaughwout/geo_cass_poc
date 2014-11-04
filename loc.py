from cassandra.cluster import Cluster
import time_uuid, datetime, time

'''
CREATE TABLE loc_hist (
  thing text,
  ts timestamp,
  lat float,
  lng float,
  temp float,
  PRIMARY KEY (thing, ts))
WITH CLUSTERING ORDER BY (ts DESC);

CREATE TABLE loc_last (
  thing text,
  ts timestamp,
  lat float,
  lng float,
  temp float,
  PRIMARY KEY (thing));

'''

## TODOs
## timeuuid
## Set time in app, not C*
## Partition by Org to avoid blanked select * kludge

KEY_SPACE = 'test'
START_LAT = 38.799578
START_LNG = -77.066955
DELTA_T = 5 # Seconds
SPEED = 10 # mps
ITER = 10
THING_ID = 'Thing 1'


lat = START_LAT
lng = START_LNG
delta_t = DELTA_T
delta_s = SPEED*3.6/110

# Connect to C*
cluster = Cluster()
session = cluster.connect(KEY_SPACE)


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