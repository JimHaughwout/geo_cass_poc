import uuid, time_uuid, datetime, time, random

def get_timeuuid(py_datetime):
    try:
        return time_uuid.TimeUUID.with_timestamp(py_datetime)
    except:
        e = "get_timeuuid: Could not convert %r to time_uuid." % py_datetime
        raise ValueError(e)

def get_iso_datetime(cassandra_uuid):
    try:
        timeuuid = time_uuid.TimeUUID.convert(cassandra_uuid)
        ts = time_uuid.TimeUUID.get_datetime(timeuuid)
        return ts.isoformat()
    except:
        e = "get_iso_datetime: Could not convert %r to ISO timestamp." % cassandra_uuid
        raise ValueError(e)

def print_location(cassandra_row):
    for loc in cassandra_row:
        print "%s is at (%.4f, %.4f) at %s" % \
         (loc.thing, loc.lat, loc.lng, get_iso_datetime(loc.ts))

now_ts = datetime.datetime.utcnow()
print now_ts, type(now_ts)

y = time_uuid.TimeUUID.with_timestamp(now_ts)
print y
#time_uuid = get_timeuuid(now_ts)
print y, type(y)

