

import pytest

from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db')


@pytest.mark.parametrize('fields', [

    # Title in surname
    dict(title='Bill Clinton', surname='Clinton'),

    # Blacklisted title (singular)
    dict(title='Letter', surname='Tolstoy'),

    # Blacklisted title (plural)
    dict(title='Letters', surname='Tolstoy'),

    # Blacklisted surname
    dict(title='War and Peace', surname='May'),

])
def test_validate(fields, add_text, add_citation):

    text = add_text(**fields)

    add_citation(text=text)

    Text.validate(
        package='osp.test.citations.models.text',
        path='fixtures/validate/validate.yml',
    )

    text = Text.get(Text.id==text.id)

    assert text.valid == False
