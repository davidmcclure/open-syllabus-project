

from redis import StrictRedis
from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *


# TODO: Make env-configurable.
postgres = PostgresqlExtDatabase('osp')
redis = StrictRedis()


class BaseModel(Model):
    class Meta:
        database = postgres
