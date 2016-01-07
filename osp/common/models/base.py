

import math

from peewee import Model, DateTimeField, fn
from playhouse.postgres_ext import ServerSide
from datetime import datetime


class BaseModel(Model):


    created = DateTimeField(default=datetime.now)


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
            cls: The next row.
        """

        row_count = cls.select().count()
        page_size = math.ceil(row_count / page_count)

        query = (
            cls.select()
            .order_by(cls.id)
            .paginate(offset+1, page_size)
        )

        for row in ServerSide(query):
            yield row


    @classmethod
    def stream(cls, page_size=10000):

        """
        Stream all rows by iterating through consecutive pages.

        Args:
            page_size (int)

        Yields:
            cls: The next row.
        """

        row_count = cls.select().count()
        page_count = math.ceil(row_count / page_size)

        for i in range(page_count):

            page = (
                cls.select()
                .order_by(cls.id)
                .paginate(i+1, page_size)
            )

            for row in page.iterator():
                yield row
