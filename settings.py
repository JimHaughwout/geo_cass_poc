from models import Bounding_Box

# Global Variables
KEY_SPACE = 'dm' # Cassandra Keyspace
ORG = 'sgs'
START_DT = '2014-11-06 20:28:00'
SPEED = 40 # kph
SPEED_VARIANCE = 10.00 # N% variance between reads
REPORTING_INTERVAL = 15 # 900 seconds between reads
THING_COUNT = 5000
TIME_VARIANCE = 5.00 # N% variance between time invervals
CYCLE_COUNT = 50
BOUNDING_BOXES = ( # Bounding boxes in UL, LR geo format
    Bounding_Box((14, -4), (6, 8)),
    Bounding_Box((1.4, 31), (0, 36)),
    Bounding_Box((1.1, 35), (-4.6, 39))
    )