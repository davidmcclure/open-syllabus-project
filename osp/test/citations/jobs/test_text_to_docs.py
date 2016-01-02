

import pytest

from osp.corpus.models import Document_Index
from osp.citations.jobs import text_to_docs
from osp.citations.models import Citation
from osp.citations.utils import tokenize_field
from peewee import fn


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_matches(add_doc, add_text):

    """
    When documents match the query, write doc -> text rows.
    """

    wp1 = add_doc(content='War and Peace, Leo Tolstoy 1')
    wp2 = add_doc(content='War and Peace, Leo Tolstoy 2')
    wp3 = add_doc(content='War and Peace, Leo Tolstoy 3')

    ak1 = add_doc(content='Anna Karenina, Leo Tolstoy 1')
    ak2 = add_doc(content='Anna Karenina, Leo Tolstoy 2')

    Document_Index.es_insert()

    text = add_text(title='War and Peace', surname='Tolstoy')
    text_to_docs(text.id)

    # Should write 3 citation links.
    assert Citation.select().count() == 3

    # Should match "War and Peace," ignore "Anna Karenina".
    for doc in [wp1, wp2, wp3]:

        assert Citation.select().where(

            Citation.text==text,
            Citation.document==doc,

            # fn.array_length(Citation.tokens, 1)==4,

            # Citation.tokens.contains([
                # 'war', 'and', 'peace', 'tolstoy',
            # ]),

        )


def test_no_matches(add_doc, add_text):

    """
    When no documents match, don't write any rows.
    """

    add_doc(content='War and Peace, Leo Tolstoy')
    Document_Index.es_insert()

    text = add_text(title='Master and Man', surname='Tolstoy')
    text_to_docs(text.id)

    # Shouldn't write any rows.
    assert Citation.select().count() == 0


@pytest.mark.parametrize('title,surname,content', [

    # Title, author.
    (
        'War and Peace',
        'Tolstoy',
        'War and Peace, Leo Tolstoy',
    ),

    # Author, title.
    (
        'War and Peace',
        'Tolstoy',
        'Leo Tolstoy, War and Peace',
    ),

    # Incomplete name.
    (
        'War and Peace',
        'Tolstoy',
        'War and Peace, Tolstoy',
    ),

])
def test_citation_formats(title, surname, content, add_doc, add_text):

    """
    Test title/author -> citation formats.
    """

    # Pad tokens around the match.
    padded = ('XXX '*1000) + content + (' XXX'*1000)

    doc = add_doc(content=padded)
    Document_Index.es_insert()

    text = add_text(title=title, surname=surname)
    text_to_docs(text.id)

    # tokens = tokenize_field(content)

    assert Citation.select().where(

        Citation.text==text,
        Citation.document==doc,

        # fn.array_length(Citation.tokens, 1)==len(tokens),
        # Citation.tokens.contains(tokens),

    )
