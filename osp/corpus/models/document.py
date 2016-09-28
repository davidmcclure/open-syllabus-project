

from osp.common import config
from osp.common.models import BaseModel
from osp.corpus.corpus import Corpus
from osp.corpus.syllabus import Syllabus

from playhouse.postgres_ext import BinaryJSONField
from peewee import CharField


class Document(BaseModel):

    # TODO: Include manifest data.

    path = CharField(unique=True)
    metadata = BinaryJSONField(default={})

    class Meta:
        database = config.get_table_db('document')

    @classmethod
    def insert_documents(cls):

        """
        Insert a document row for each syllabus in the corpus.
        """

        for syllabus in Corpus.from_env().syllabi_bar():
            try:cls.create(path=syllabus.relative_path)
            except: pass

    def syllabus(self):

        """
        Wrap the row as an OSP Syllabus instance.
        """

        return Syllabus.from_env(self.path)
