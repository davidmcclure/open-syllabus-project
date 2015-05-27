

import re

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import query_bar
from osp.corpus.models.document import Document
from osp.corpus.models.text import Document_Text
from osp.citations.hlom.models.citation import HLOM_Citation
from playhouse.postgres_ext import TSVectorField
from peewee import *


class Document_Search(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    text = TSVectorField()


    class Meta:
        database = config.get_table_db('document_search')


    @classmethod
    def index(cls):

        """
        Copy in document text values.
        """

        cited = (

            Document_Text.select()
            .group_by(Document_Text.id)

            # Join the citations.
            .join(HLOM_Citation, on=(
                Document_Text.document==HLOM_Citation.document
            ))

        )

        for t in query_bar(cited):

            try:
                cls.create(
                    document=t._data['document'],
                    text=fn.to_tsvector(t.text)
                )

            except: pass
