

from playhouse.postgres_ext import ServerSide

from osp.institutions.utils import seed_to_regex
from osp.institutions.models import Institution


# TODO|dev
class DocInstWorker:

    def __init__(self):

        """
        Initialize the regex -> institution map.
        """

        self.regex_to_inst = [
            (seed_to_regex(inst.url), inst)
            for inst in ServerSide(Institution.select())
            if inst.url
        ]

    def __call__(self, document):

        """
        Match a document URL to an institution, write a link row.

        Args:
            document (Document)
        """

        pass
