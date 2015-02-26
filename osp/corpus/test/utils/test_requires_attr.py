

import pytest

from osp.corpus.utils import requires_attr


class Test:
    @requires_attr('attr')
    def needs_attr(self):
        return True


@pytest.fixture
def instance():
    return Test()


def test_attr_does_not_exist(instance):
    """
    If the required attribute is missing, return None.
    """
    assert instance.needs_attr() == None


def test_attr_exists(instance):
    """
    If the required attribute is present, run the method.
    """
    instance.attr = True
    assert instance.needs_attr() == True
