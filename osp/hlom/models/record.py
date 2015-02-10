

from osp.common.models.base import LocalModel
from peewee import *
from functools import lru_cache
from playhouse.postgres_ext import *
from pymarc import Record


class HLOM_Record(LocalModel):


    control_number = CharField(unique=True)
    record = BlobField()


    @property
    @lru_cache()
    def pymarc(self):

        """
        Wrap the raw record blob as a Pymarc record instance.
        """

        return Record(
            data=bytes(self.record),
            ascii_handling='ignore',
            utf8_handling='ignore'
        )
