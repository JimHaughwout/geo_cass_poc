import settings
from datetime import datetime, timedelta
from time import sleep
from random import uniform
from models import Loc_Read
from map_utils import gen_map
from cassandra.cluster import Cluster
from time_utils import make_timeuuid

def move_thing(thing, speed, variance, clock_ts):
    # deg / km * km / hr * hr / sec * sec
    elapsed_seconds = (clock_ts - thing.ts).total_seconds()
    deg_move = (1 / 110.4) * speed * (1.0 / 3600) * elapsed_seconds
    lat_move = uniform(0, 1) * deg_move * uniform(100 - variance, 100 + variance) / 100
    lng_move = uniform(0, 1) * deg_move * uniform(100 - variance, 100 + variance) / 100
    if thing.id % 4 == 0: 
        thing.lat += lat_move
        thing.lng += lng_move
    elif thing.id % 4 == 1:
        thing.lat += lat_move
        thing.lng -= lng_move 
    elif thing.id % 4 == 2:
        thing.lat -= lat_move
        thing.lng -= lng_move           
    else:
        thing.lat -= lat_move
        thing.lng += lng_move 
    thing.ts += timedelta(seconds=elapsed_seconds)

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

CREATE TABLE loc_dash (
  org text,
  thing text,
  ts timestamp,
  lat float,
  lng float,
  PRIMARY KEY (org, thing))
WITH CLUSTERING ORDER BY (thing ASC);

'''
insert_loc_hist = session.prepare("INSERT INTO loc_hist (org, thing, ts_id, lat, lng) VALUES (?, ?, ?, ?, ?)")
insert_loc_dash = session.prepare("INSERT INTO loc_dash (org, thing, ts, lat, lng) VALUES (?, ?, ?, ?, ?) USING TTL 3600")


# Generated Derived Variables
read_interval = float(settings.REPORTING_INTERVAL) / settings.THING_COUNT
clock_ts = datetime.strptime(settings.START_DT, "%Y-%m-%d %H:%M:%S")
interval_lo = (1.0 - settings.TIME_VARIANCE / 100.0) * read_interval
interval_hi = (1.0 + settings.TIME_VARIANCE / 100.0) * read_interval
# print interval_lo, interval_hi

# Build array of initial thing locations
thing_state = []
for thing in xrange(1, settings.THING_COUNT + 1):
    box = settings.BOUNDING_BOXES[thing % len(settings.BOUNDING_BOXES)]
    clock_ts += timedelta(seconds=uniform(interval_lo, interval_hi))
    start_lat, start_lng = box.get_start_coords()
    starting_loc = Loc_Read(int(thing), clock_ts, start_lat, start_lng)
    thing_state.append(starting_loc)


# Generate movements and reads for CYCLE_COUNT passes through all things
i = 1
for cycle in xrange(0, settings.CYCLE_COUNT):
    for thing in thing_state:
        print i # Show activity
        i += 1

        # Generate a delay and increment the virtual clock
        time_interval = uniform(interval_lo, interval_hi)
        sleep(time_interval)
        clock_ts += timedelta(seconds=time_interval)
        
        # Simulate the move, in memory
        move_thing(thing, settings.SPEED, settings.SPEED_VARIANCE, clock_ts)
        
        # Insert in-memory values into Cassandra
        try:
          session.execute(insert_loc_hist, [str(settings.ORG), str(thing.id), make_timeuuid(thing.ts), thing.lat, thing.lng])
        except:
          print "Could not insert location history for Thing %d at %s" % (thing.id, thing.ts)
        try:
          session.execute(insert_loc_dash, [str(settings.ORG), str(thing.id), thing.ts, thing.lat, thing.lng])
        except:
          print "Could not insert into location dashboard for Thing %d at %s" % (thing.id, thing.ts)

# Close Cassandra session
session.shutdown()



