

import datetime

from peewee import Model, DateTimeField, fn


class BaseModel(Model):


    created = DateTimeField(default=datetime.datetime.now)


    @classmethod
    def reload(cls, model):

        """
        Reload a model instance. (Used in testing.)

        Args:
            model (peewee.Model)

        Returns: cls
        """

        return cls.get(cls.id==model.id)


    @classmethod
    def max_id(cls):

        """
        Get the max id on the table.

        Returns: int
        """

        return cls.select(fn.Max(cls.id)).scalar()
