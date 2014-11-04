from datetime import datetime, timedelta
from time_utils import *

clock_time = datetime.now()
event_id = make_timeuuid(clock_time)
event_ts = get_ts_for_timeuuid(event_id, iso=True)

print clock_time, type(clock_time)
print event_id, type(event_id)
print event_ts, type(event_ts)