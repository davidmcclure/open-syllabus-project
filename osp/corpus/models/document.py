

from osp.common.models.base import BaseModel
from peewee import *


class Document(BaseModel):


    path = CharField(unique=True)
    stored_id = BigIntegerField(null=True)
    metadata = HStoreField()


    @classmethod
    def exists(cls, path):

        """
        Does a row for a given path exist?

        :param path: The corpus-relative path.
        """

        return cls.select().where(cls.path==path).exists()


    class Meta:
        db_name = 'document'
