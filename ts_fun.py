#!/usr/bin/python

import sys
import socket
import csv
from datetime import datetime, timedelta
from time import mktime
from random import randint, uniform

from time_uuid import TimeUUID

# Parameters
clock_time = datetime.now()
data_points = 10
num_sensors = 4
sec_btw_reads = 15

# Schema Inputs
org = socket.gethostname()
group = sys.argv[1]
thing_type = sys.argv[2]
#thing_id = thing_type + '-001'

with open('%s-%s.csv' % (group, thing_type), 'wb') as csvfile:
    wrtr = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for cycle in xrange(data_points):
        clock_time -= timedelta(seconds=sec_btw_reads)
        for sensor in xrange(num_sensors):
            event_time  = clock_time + timedelta(seconds=uniform(-2.5,2.5))
            event_ts = event_time.strftime("%Y-%m-%d %H:%M:%S%Z")
            event_id = TimeUUID.with_timestamp(mktime(event_time.timetuple()), randomize=True)

            temp = uniform(18,20.1)
            thing_id = "%s-%03d" % (thing_type, sensor + 1)

            print "%s, %s, %s, %s, %s, %s" % (org, group, thing_id, event_id, event_ts, temp)
            wrtr.writerow([org, group, thing_id, event_id, event_ts, temp])