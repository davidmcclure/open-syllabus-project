

import pytest

from osp.corpus.models.text import Document_Text
from osp.fields.models.field import Field
from osp.fields.models.field_document import Field_Document
from osp.fields.jobs.query import query


@pytest.mark.fields
def test_match_secondary_fields(corpus_index, add_doc):
    pass
