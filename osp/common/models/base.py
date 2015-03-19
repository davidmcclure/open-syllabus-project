

import datetime

from peewee import Model, DateTimeField


class BaseModel(Model):
    created = DateTimeField(default=datetime.datetime.now)
