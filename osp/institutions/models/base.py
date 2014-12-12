

from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *


# TODO: Make env-configurable.
database = PostgresqlExtDatabase('osp')


class BaseModel(Model):


    @classmethod
    def join_metadata(cls, metadata):

        """
        Join on the most recent rows from a metadata table.

        :param Model metadata: The metadata model.
        """

        return (
            cls
            .select(cls, metadata)
            .distinct([cls.id])
            .join(metadata, JOIN_LEFT_OUTER)
            .order_by(cls.id, metadata.created.desc())
        )


    class Meta:
        database = database
