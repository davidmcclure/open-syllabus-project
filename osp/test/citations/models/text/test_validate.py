

import pytest

from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db')


@pytest.mark.parametrize('fields', [

    # Title and author overlap
    dict(title='Elvis', authors=['Presley, Elvis']),

    # Blacklisted title (singular)
    dict(title='Letter'),

    # Blacklisted title (plural)
    dict(title='Letters'),

    # Blacklisted surname
    dict(surname='May'),

    # Toponym title
    dict(title='Texas'),

    # Toponym surname
    dict(surname='Texas'),

    # Unfocused
    dict(title='Ideas', surname='Young'),

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


def test_whitelist(add_text, add_citation):

    """
    Whitelisted texts should be exempt from the fuzziness cutoff.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    add_citation(text=t1)
    add_citation(text=t2)
    add_citation(text=t3)

    Text.validate(
        package='osp.test.citations.models.text',
        path='fixtures/validate/whitelist.yml',
    )

    t1 = Text.get(Text.id==t1.id)
    t2 = Text.get(Text.id==t2.id)
    t3 = Text.get(Text.id==t3.id)

    assert t1.valid == True
    assert t2.valid == True
    assert t3.valid == False
