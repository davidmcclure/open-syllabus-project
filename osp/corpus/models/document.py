

from osp.corpus.syllabus import Syllabus
from playhouse.postgres_ext import *
from osp.common.models.base import LocalModel
from peewee import *


class Document(LocalModel):


    stored_id = BigIntegerField(null=True)
    path = CharField(unique=True)


    @property
    def syllabus(self):

        """
        Wrap the row as an OSP Syllabus instance.
        """

        pass
