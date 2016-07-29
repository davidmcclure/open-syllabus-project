

from peewee import ForeignKeyField
from playhouse.postgres_ext import ServerSide

from osp.common import config
from osp.common.models.base import BaseModel
from osp.institutions.models import Institution
from osp.institutions.utils import seed_to_regex
from osp.corpus.models import Document
from osp.corpus.corpus import Corpus


class Institution_Document(BaseModel):


    institution = ForeignKeyField(Institution)
    document = ForeignKeyField(Document)


    class Meta:
        database = config.get_table_db('institution_document')


    @classmethod
    def link(cls):

        """
        Try to link each document with an institution.
        """

        # TODO: multiprocessing?

        # get (regex, inst id) list
        # loop through docs
        # check each doc against each regex
        # on match, write link row

        regex_to_id = [
            (seed_to_regex(i.url), i.id)
            for i in ServerSide(Institution.select())
            if i.url
        ]

        corpus = Corpus.from_env()

        for i, syllabus in enumerate(corpus.syllabi()):

            for pattern, id in regex_to_id:
                if pattern.search(syllabus.url):
                    break

            if i%1000 == 0:
                print(i)
