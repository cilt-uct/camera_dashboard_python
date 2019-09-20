from mongoengine import Document
from mongoengine.fields import StringField, DateTimeField


class Venues(Document):
    venue_name = StringField(null=False)
    status = StringField(null=False)
    cam_url = StringField(null=False)
    last_updated = DateTimeField(null=False)
    sync_time = DateTimeField(null=False)


class VenueDict(object):
    def __init__(self, a, b, c, d, e):
        self.venue_name = a
        self.status = b
        self.cam_url = c
        self.last_updated = d
        self.sync_time = e

    def __iter__(self):
        return iter([('venue_name', self.venue_name),
                     ('status', self.status),
                     ('cam_url', self.cam_url),
                     ('last_updated', self.last_updated),
                     ('sync_time', self.sync_time)
                     ])
