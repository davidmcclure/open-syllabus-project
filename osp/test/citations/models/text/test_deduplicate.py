

import pytest

from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db', 'redis')


def test_deduplicate(add_text, add_citation):

    """
    Text.deduplicate() set `display` flags for all cited texts.
    """

    t1 = add_text(title='one', surname='two')
    t2 = add_text(title='one', surname='two')

    t3 = add_text(title='three', surname='four')
    t4 = add_text(title='three', surname='four')

    t5 = add_text(title='five', surname='six')

    add_citation(text=t1)
    add_citation(text=t2)
    add_citation(text=t3)
    add_citation(text=t4)
    add_citation(text=t5)

    Text.deduplicate()

    t1 = Text.get(Text.id==t1.id)
    t2 = Text.get(Text.id==t2.id)
    t3 = Text.get(Text.id==t3.id)
    t4 = Text.get(Text.id==t4.id)
    t5 = Text.get(Text.id==t5.id)

    assert t1.display == True
    assert t2.display == False

    assert t3.display == True
    assert t4.display == False

    assert t5.display == True
