

from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *


# TODO: Make env-configurable.
database = PostgresqlExtDatabase('osp')


class BaseModel(Model):
    class Meta:
        database = database
