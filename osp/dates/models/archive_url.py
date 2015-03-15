

import time

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from datetime import datetime
from peewee import *


class Document_Date_Archive_Url(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    timestamp = CharField(index=True)


    @property
    def date(self):

        """
        Convert the raw timestamp into a datetime instance.
        """

        return datetime.strptime(
            self.timestamp,
            '%Y%m%d%H%M%S'
        )


    class Meta:
        database = config.get_table_db('document_date_archive_url')
