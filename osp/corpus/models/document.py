

from osp.common.config import config
from osp.corpus.syllabus import Syllabus
from peewee import *


class Document(Model):


    stored_id = BigIntegerField(null=True)
    path = CharField(unique=True)


    @property
    def syllabus(self):

        """
        Wrap the row as an OSP Syllabus instance.
        """

        return Syllabus.from_env(self.path)


    class Meta:
        database = config.get_db('document')
