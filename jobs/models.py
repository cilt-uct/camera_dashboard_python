from mongoengine import Document
from mongoengine.fields import StringField, DateTimeField, BooleanField


class Venues(Document):
    venue_name = StringField(null=False)
    status = StringField(null=False)
    cam_url = StringField(null=False)
    last_updated = DateTimeField(null=False)
    sync_time = DateTimeField(null=False)
    regularly_updating = BooleanField(null=False)
