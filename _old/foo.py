from time_uuid import TimeUUID
from time import mktime
from datetime import datetime, timedelta

def make_timeuuid(event_time):
    '''
    Creates a randomized time_uuid.TimeUUID for a given datetime.datetime.
    '''
    try:        
        return TimeUUID.with_timestamp(
            mktime(event_time.timetuple()), randomize=True)
    except:
        e = "get_event_id: %r is not a datetime.datetime, is %r." % \
         (event_time, type(event_time))
        raise ValueError(e)


def get_ts_for_timeuuid(timeuuid, iso=False):
    try:
        ts = TimeUUID.get_datetime(timeuuid)
    except:
        e = "get_ts_for_timeuuid: %r is not a time_uuid.TimeUUID, is %r." % \
         (timeuuid, type(timeuuid))
        raise ValueError(e)
    if iso:
        return ts.isoformat()
    else:     
        return ts

clock_time = datetime.now()
event_id = make_timeuuid(clock_time)
event_ts = get_ts_for_timeuuid(event_id, iso=True)

print clock_time, type(clock_time)
print event_id, type(event_id)
print event_ts, type(event_ts)
