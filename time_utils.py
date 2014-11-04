from time_uuid import TimeUUID
from time import mktime
from datetime import datetime, timedelta

def make_timeuuid(event_time):
    '''
    Creates a randomized time_uuid.TimeUUID for a given datetime.datetime

    :param event_time: datetime.datetime to get timeuuid for
    :retuens: time_uuid.TimeUUID

    '''
    try:        
        return TimeUUID.with_timestamp(
            mktime(event_time.timetuple()), randomize=True)
    except:
        e = "get_event_id: %r is not a datetime.datetime, is %r." % \
         (event_time, type(event_time))
        raise ValueError(e)


def get_ts_for_timeuuid(timeuuid, cassandra=False, iso=False):
    '''
    Extracts timestamp from TimeUUID.
    By default, returns datetime.datetime.
    Returns iso 8166 timestamp string if iso == True
    '''
    try:
        if cassandra == True:
            timeuuid = TimeUUID.convert(timeuuid)
        ts = TimeUUID.get_datetime(timeuuid)
    except:
        e = "get_ts_for_timeuuid: %r is not a time_uuid.TimeUUID, is %r." % \
         (timeuuid, type(timeuuid))
        raise ValueError(e)
    if iso:
        return ts.isoformat()
    else:     
        return ts
