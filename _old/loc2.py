from cassandra.cluster import Cluster
import uuid, time_uuid, datetime, time

KEY_SPACE = 'dm'

'''
CREATE TABLE loc_hist (
  thing text,
  ts_id timeuuid,
  lat float,
  lng float,
  temp float,
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

## TODOs
## timeuuid
## Set time in app, not C*
## Partition by Org to avoid blanked select * kludge

# Connect to C*
cluster = Cluster()
session = cluster.connect(KEY_SPACE)

# Prepare statements
get_loc_stmt = session.prepare("SELECT * FROM loc_hist")

locations = session.execute(get_loc_stmt)
#for location in locations:
#  for loc in location:
#    print loc, type(loc)
print locations[0]
print locations[0].ts_id
foo = time_uuid.TimeUUID.convert(locations[0].ts_id)
bar = time_uuid.TimeUUID.get_datetime(foo)
print bar.isoformat()

x = datetime.datetime.utcnow()
print x
y = time_uuid.TimeUUID.with_timestamp(x)
print y

'''
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