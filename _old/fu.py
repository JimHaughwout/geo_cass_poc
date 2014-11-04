from datetime import datetime, timedelta
from time import sleep
from random import uniform

class Loc_Read(object):

    def __init__(self, thing_id, timestamp, latitude, longitude):
        self.id = thing_id
        self.ts = timestamp # 
        self.lat = float(latitude)
        self.lng = float(longitude)


class Bounding_Box(object):

    def __init__(self, upper_left_coords, lower_right_coords):
        self.lat_n, self.lng_w = upper_left_coords
        self.lat_s, self.lng_e = lower_right_coords

    def get_start_coords(self):
        lat = uniform(self.lat_s, self.lat_n)
        lng = uniform(self.lng_w, self.lng_e)
        return lat, lng


def gen_google_coords(locations):
    for location in thing_locations:
        print "          [%.4f, %.4f, 'Thing-%s @ %s']," % \
         (location.lat, location.lng, location.id, location.ts)

def move_thing(thing, speed, variance, clock_ts):
    # deg / km * km / hr * hr / sec * sec
    elapsed_seconds = (clock_ts - thing.ts).total_seconds()
    print elapsed_seconds
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

# Global Variables
START_DT = '2014-11-02 23:15:15'
SPEED = 40 # kph
SPEED_VARIANCE = 10.00 # N% variance between reads
REPORTING_INTERVAL = 900 # 900 seconds between reads
THING_COUNT = 10
TIME_VARIANCE = 5.00 # N% variance between time invervals
CYCLE_COUNT = 1
BOUNDING_BOXES = ( # Bounding boxes in UL, LR geo format
    Bounding_Box((14, -4), (6, 8)),
    Bounding_Box((1.4, 31), (0, 36)),
    Bounding_Box((1.1, 35), (-4.6, 39))
    )

# Derived Variables
read_interval = float(REPORTING_INTERVAL) / THING_COUNT
clock_ts = datetime.strptime(START_DT, "%Y-%m-%d %H:%M:%S")
interval_lo = (1.0 - TIME_VARIANCE / 100.0) * read_interval
interval_hi = (1.0 + TIME_VARIANCE / 100.0) * read_interval
print interval_lo, interval_hi

# Build array of initial thing locations
thing_state = []
for thing in xrange(1, THING_COUNT + 1):
    box = BOUNDING_BOXES[thing % len(BOUNDING_BOXES)]
    clock_ts += timedelta(seconds=uniform(interval_lo, interval_hi))
    start_lat, start_lng = box.get_start_coords()
    starting_loc = Loc_Read(int(thing), clock_ts, start_lat, start_lng)
    thing_state.append(starting_loc)

# Start moving
for cycle in xrange(0, CYCLE_COUNT):
    for thing in thing_state:
        clock_ts += timedelta(seconds=uniform(interval_lo, interval_hi))
        move_thing(thing, SPEED, SPEED_VARIANCE, clock_ts)
        print thing.id, thing.lat, thing.lng, thing.ts



