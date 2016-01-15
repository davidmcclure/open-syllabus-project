

from osp.common import config

from osp.citations.models import Citation_Index
from osp.citations.models import Text_Index
from osp.institutions.models import Institution_Index
from osp.fields.models import Field_Index
from osp.fields.models import Subfield_Index


def index_elasticsearch():

    """
    Populate public-facing Elasticsearch indexes.
    """

    for index in [
        Citation_Index,
        Text_Index,
        Subfield_Index,
        Field_Index,
        Institution_Index,
    ]:

        index.es_insert()
