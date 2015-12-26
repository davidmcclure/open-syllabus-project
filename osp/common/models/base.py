

import datetime
import math

from peewee import Model, DateTimeField, fn
from playhouse.postgres_ext import ServerSide


class BaseModel(Model):


    created = DateTimeField(default=datetime.datetime.now)


    @classmethod
    def max_id(cls):

        """
        Get the max id on the table.

        Returns: int
        """

        return cls.select(fn.Max(cls.id)).scalar()


    @classmethod
    def page_cursor(cls, page_count, offset):

        """
        Generate id-ordered model instances in a "page," defined by a total
        page count and a 0-indexed offset.

        Args:
            page_count (int): Total pages.
            offset (int): 0-indexed page offset.

        Yields:
            cls: The next instance.
        """

        total_count = cls.select().count()
        page_size = math.ceil(total_count / page_count)

        query = (
            cls.select()
            .order_by(cls.id)
            .paginate(offset+1, page_size)
        )

        for row in ServerSide(query):
            yield row
