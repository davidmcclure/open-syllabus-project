

import pytest

from osp.institutions.models import Institution_Document
from peewee import IntegrityError


pytestmark = pytest.mark.usefixtures('db')


def test_unique_pairs(add_doc, add_institution):

    """
    Don't allow duplicate links between the same doc -> inst pair.
    """

    inst = add_institution()

    doc = add_doc()

    Institution_Document.create(
        institution=inst,
        document=doc,
    )

    with pytest.raises(IntegrityError):

        Institution_Document.create(
            institution=inst,
            document=doc,
        )
