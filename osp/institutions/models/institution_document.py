

from peewee import ForeignKeyField
from playhouse.postgres_ext import ServerSide

from osp.common import config
from osp.common.utils import parse_domain, query_bar
from osp.common.models import BaseModel
from osp.institutions.models import Institution
from osp.corpus.models import Document


class Institution_Document(BaseModel):


    institution = ForeignKeyField(Institution)
    document = ForeignKeyField(Document)


    class Meta:
        database = config.get_table_db('institution_document')


    @classmethod
    def link(cls):

        """
        Link documents -> institutions.
        """

        domain_to_inst = {
            parse_domain(inst.url): inst
            for inst in ServerSide(Institution.select())
            if inst.url
        }

        for doc in query_bar(Document.select()):

            try:

                domain = parse_domain(doc.syllabus.url)

                # Write the link row.
                cls.create(
                    institution=domain_to_inst[domain],
                    document=doc,
                )

            except Exception as e:
                print(e)
