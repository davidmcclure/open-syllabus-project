

import peewee
import pytest

from osp.institutions.models.institution import Institution


def test_unique_name_website(models):

    """
    Name / website pairs should be unique.
    """

    Institution.create(name='name', website='website')

    with pytest.raises(peewee.IntegrityError):
        Institution.create(name='name', website='website')
