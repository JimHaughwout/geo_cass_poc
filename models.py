from random import uniform

class Loc_Read(object):
    '''
    Location Read object:

    @param: id - Thing ID  
    @param: ts - Timestamp of Read (datetime.datetime)
    @param: lat - Latitude of read location
    @param: lng - Longitude of read location
    '''

    def __init__(self, thing_id, timestamp, latitude, longitude):
        self.id = thing_id
        self.ts = timestamp # 
        self.lat = float(latitude)
        self.lng = float(longitude)


class Bounding_Box(object):
    '''
    Geographic bounding box. We use this to select random start points
    between upper-left (Northwest corner) and lower-right (Southeast corner)
    '''

    def __init__(self, upper_left_coords, lower_right_coords):
        self.lat_n, self.lng_w = upper_left_coords
        self.lat_s, self.lng_e = lower_right_coords

    def get_start_coords(self):
        lat = uniform(self.lat_s, self.lat_n)
        lng = uniform(self.lng_w, self.lng_e)
        return lat, lng