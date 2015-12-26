

import datetime
import math

from peewee import Model, DateTimeField, fn
from playhouse.postgres_ext import ServerSide


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


    @classmethod
    def page_cursor(cls, total_pages, page_index):

        """
        Given a worker count and index, generate a page of records.

        Args:
            total_pages (int): The total number of pages.
            page_index (int): 0-based page index.

        Yields:
            cls: The next record.
        """

        count = cls.select().count()
        page_size = math.ceil(count / total_pages)

        query = (
            cls.select()
            .order_by(cls.id)
            .paginate(page_index+1, page_size)
        )

        for row in ServerSide(query):
            yield row
