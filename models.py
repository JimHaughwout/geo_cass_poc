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