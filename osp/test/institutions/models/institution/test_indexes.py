

import peewee
import pytest

from osp.institutions.models import Institution


def test_unique_domain(models):

    """
    Domains should be unique.
    """

    Institution.create(name='name1', domain='test.edu')

    with pytest.raises(peewee.IntegrityError):
        Institution.create(name='name2', website='test.edu')
