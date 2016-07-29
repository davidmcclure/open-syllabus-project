

from peewee import ForeignKeyField
from playhouse.postgres_ext import ServerSide

from osp.common import config
from osp.common.models.base import BaseModel
from osp.common.utils import query_bar
from osp.institutions.models import Institution
from osp.institutions.utils import seed_to_regex
from osp.corpus.models import Document


class Institution_Document(BaseModel):


    institution = ForeignKeyField(Institution)
    document = ForeignKeyField(Document)


    class Meta:
        database = config.get_table_db('institution_document')


    @classmethod
    def link(cls):

        """
        Link each document with an institution.
        """

        # TODO: multiprocessing?

        # Map URL regex -> institution.
        regex_to_inst = [
            (seed_to_regex(inst.url), inst)
            for inst in ServerSide(Institution.select())
            if inst.url
        ]

        docs = query_bar(Document.select())

        # Walk documents.
        for i, doc in enumerate(docs):

            # Probe for a matching institution.
            for regex, inst in regex_to_inst:
                if regex.search(doc.syllabus.url):

                    # Write the link row.
                    cls.create(institution=inst, document=doc)
