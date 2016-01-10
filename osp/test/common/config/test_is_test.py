

import pytest

from .conftest import get_config


@pytest.mark.parametrize('fixture,is_test', [
    ('true', True),
    ('no-key', False),
    ('false', False),
])
def test_is_test(fixture, is_test):

    config = get_config('is_test/{0}'.format(fixture))

    assert config.is_test() == is_test
