

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.syllabus import Syllabus
from playhouse.postgres_ext import BinaryJSONField
from peewee import *


class Document(BaseModel):


    path = CharField(unique=True)
    metadata = BinaryJSONField()


    @property
    def syllabus(self):

        """
        Wrap the row as an OSP Syllabus instance.
        """

        return Syllabus.from_env(self.path)


    class Meta:
        database = config.get_db('document')
