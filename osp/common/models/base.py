

from redis import StrictRedis
from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *
from elasticsearch import Elasticsearch


# TODO: Make env-configurable.
postgres = PostgresqlExtDatabase('osp')
redis = StrictRedis()
elasticsearch = Elasticsearch()



class BaseModel(Model):
    class Meta:
        database = postgres
