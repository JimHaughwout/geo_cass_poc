from datetime import datetime, timedelta
from time import sleep
from random import uniform
import settings
from models import Loc_Read
from map_utils import gen_map
from cassandra.cluster import Cluster


def move_thing(thing, speed, variance, clock_ts):
    # deg / km * km / hr * hr / sec * sec
    elapsed_seconds = (clock_ts - thing.ts).total_seconds()
    #print elapsed_seconds
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
luster = Cluster()
session = cluster.connect(settings.KEY_SPACE)


# Derived Variables
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


# Start moving
for cycle in xrange(0, settings.CYCLE_COUNT):
    for thing in thing_state:
        clock_ts += timedelta(seconds=uniform(interval_lo, interval_hi))
        move_thing(thing, settings.SPEED, settings.SPEED_VARIANCE, clock_ts)
        # print thing.id, thing.lat, thing.lng, thing.ts

#Trigger the map
gen_map(thing_state)



