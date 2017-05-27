###
# Model used for coordinates, not used atm because Gustaf is a hater
# It's working (Confirmed) but not used because of reason above
###
from urllib.parse import urlencode
import json

class Coordinates(object):
    id = 0
    x = 0
    y = 0

    def __init__(self, id,  x, y):
        self.id = id
        self.x = x
        self.y = y

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=(':',':'))

    #def as_dict(self):
    #    return {'id' : self.id, 'x' : self.x, 'y' : self.y}
