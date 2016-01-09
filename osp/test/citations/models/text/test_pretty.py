

import pytest

from osp.citations.models import Text
from osp.common.utils import prettify


def test_string_field():

    """
    Text#pretty() should return a prettified version of the field.
    """

    text = Text(title='war and peace')

    assert text.pretty('title') == prettify('war and peace')


def test_array_field():

    """
    If the requested field is an array, prettify each element.
    """

    text = Text(authors=[
        'david mcclure',
        'joe karaganis',
    ])

    assert text.pretty('authors') == [
        prettify('david mcclure'),
        prettify('joe karaganis'),
    ]
