

import datetime

from peewee import Model, DateTimeField


class BaseModel(Model):


    created = DateTimeField(default=datetime.datetime.now)


    @classmethod
    def reload(cls, model):

        """
        Reload a model instance. (Used in testing.)

        args:
            model (peewee.Model)
        """

        return cls.get(cls.id==model.id)
