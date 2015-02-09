

from osp.common.models.base import WorkerModel
from peewee import *
from playhouse.postgres_ext import *
from pymarc import Record


class HLOM_Record(WorkerModel):


    control_number = CharField(unique=True)
    record = BlobField()


    def pymarc_record(self):

        """
        Wrap the raw record blob as a Pymarc record instance.
        """

        return Record(
            data=bytes(self.record),
            ascii_handling='ignore',
            utf8_handling='ignore'
        )
