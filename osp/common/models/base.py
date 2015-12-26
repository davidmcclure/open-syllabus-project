

import datetime

from peewee import Model, DateTimeField, fn


class BaseModel(Model):


    created = DateTimeField(default=datetime.datetime.now)


    @classmethod
    def max_id(cls):

        """
        Get the max id on the table.

        Returns: int
        """

        return cls.select(fn.Max(cls.id)).scalar()
