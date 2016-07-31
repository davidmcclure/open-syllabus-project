

from peewee import ForeignKeyField
from playhouse.postgres_ext import ServerSide

from osp.common import config
from osp.common.utils import parse_domain
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

        return domain_to_inst
