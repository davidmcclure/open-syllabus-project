

import pytest

from osp.corpus.models import Document_Text
from osp.citations.jobs import text_to_docs
from osp.citations.models import Citation
from osp.citations.utils import get_min_freq

from peewee import fn


@pytest.mark.parametrize('title,author,content', [

    # Title, author.
    (
        'War and Peace',
        'Leo Tolstoy',
        'War and Peace, Leo Tolstoy',
    ),

    # Author, title.
    (
        'War and Peace',
        'Leo Tolstoy',
        'Leo Tolstoy, War and Peace',
    ),

    # Incomplete name.
    (
        'War and Peace',
        'Leo Tolstoy',
        'War and Peace, Tolstoy',
    ),

])
def test_matches(title, author, content, corpus_index, add_doc, add_text):

    """
    Test title/author -> citation matches.
    """

    # Pad tokens around the match.
    content = ('XXX '*1000) + content + (' XXX'*1000)

    doc = add_doc(content=content)
    Document_Text.es_insert()

    text = add_text(title=title, author=author)
    text_to_docs(text.id)

    assert Citation.select().where(
        Citation.text==text,
        Citation.document==doc,
    )


def test_multiple_matches(corpus_index, add_doc, add_text):

    """
    When OSP documents match the query, write link rows.
    """

    d1 = add_doc(content='War and Peace, Leo Tolstoy 1')
    d2 = add_doc(content='War and Peace, Leo Tolstoy 2')
    d3 = add_doc(content='War and Peace, Leo Tolstoy 3')
    d4 = add_doc(content='Anna Karenina, Leo Tolstoy 1')
    d5 = add_doc(content='Anna Karenina, Leo Tolstoy 2')

    Document_Text.es_insert()

    text = add_text(title='War and Peace', author='Leo Tolstoy')
    text_to_docs(text.id)

    # Should write 3 citation links.
    assert Citation.select().count() == 3

    # Should match the right documents.
    for doc in [d1, d2, d3]:

        assert Citation.select().where(
            Citation.text==text,
            Citation.document==doc,
        )


def test_no_matches(corpus_index, add_doc, add_text):

    """
    When no documents match, don't write any rows.
    """

    add_doc(content='War and Peace, Leo Tolstoy')
    Document_Text.es_insert()

    text = add_text(title='Master and Man', author='Leo Tolstoy')
    text_to_docs(text.id)

    # Shouldn't write any rows.
    assert Citation.select().count() == 0


def test_min_freq(corpus_index, add_doc, add_text):

    """
    Each citation should be stored with a "minimum frequency" score - the
    min_freq of the lowest-scoring query that matched the document.
    """

    # this/that > one > two > three

    d1 = add_doc(content='This That, One Two Three')
    d2 = add_doc(content='This That, One')
    d3 = add_doc(content='This That, Two')
    d4 = add_doc(content='This That, Three')

    Document_Text.es_insert()

    text = add_text(title='This That', author='One Two Three')
    text_to_docs(text.id)

    for doc, tokens in [
        (d1, ['one', 'two', 'three']),
        (d2, ['one']),
        (d3, ['two']),
        (d4, ['three']),
    ]:

        assert Citation.select().where(

            Citation.text==text,
            Citation.document==doc,

            fn.round(Citation.min_freq.cast('numeric'), 2) == \
            round(get_min_freq(tokens), 2),

        )
