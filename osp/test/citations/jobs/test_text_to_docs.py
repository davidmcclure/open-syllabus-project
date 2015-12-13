

import pytest

from osp.corpus.models import Document_Text
from osp.citations.jobs import text_to_docs
from osp.citations.models import Citation
from osp.citations.utils import get_min_freq, tokenize_field

from peewee import fn


def test_matches(corpus_index, add_doc, add_text):

    """
    When documents match the query, write doc -> text rows.
    """

    wp1 = add_doc(content='War and Peace, Leo Tolstoy 1')
    wp2 = add_doc(content='War and Peace, Leo Tolstoy 2')
    wp3 = add_doc(content='War and Peace, Leo Tolstoy 3')

    ak1 = add_doc(content='Anna Karenina, Leo Tolstoy 1')
    ak2 = add_doc(content='Anna Karenina, Leo Tolstoy 2')

    Document_Text.es_insert()

    text = add_text(title='War and Peace', authors=['Leo Tolstoy'])
    text_to_docs(text.id)

    # Should write 3 citation links.
    assert Citation.select().count() == 3

    # Should match "War and Peace," ignore "Anna Karenina".
    for doc in [wp1, wp2, wp3]:

        assert Citation.select().where(

            Citation.text==text,
            Citation.document==doc,

            fn.array_length(Citation.tokens, 1)==5,

            Citation.tokens.contains([
                'war', 'and', 'peace', 'leo', 'tolstoy',
            ]),

        )


def test_no_matches(corpus_index, add_doc, add_text):

    """
    When no documents match, don't write any rows.
    """

    add_doc(content='War and Peace, Leo Tolstoy')
    Document_Text.es_insert()

    text = add_text(title='Master and Man', authors=['Leo Tolstoy'])
    text_to_docs(text.id)

    # Shouldn't write any rows.
    assert Citation.select().count() == 0


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
def test_citation_formats(title, author, content,
        corpus_index, add_doc, add_text):

    """
    Test title/author -> citation formats.
    """

    # Pad tokens around the match.
    padded = ('XXX '*1000) + content + (' XXX'*1000)

    doc = add_doc(content=padded)
    Document_Text.es_insert()

    text = add_text(title=title, authors=[author])
    text_to_docs(text.id)

    tokens = tokenize_field(content)

    assert Citation.select().where(

        Citation.text==text,
        Citation.document==doc,

        fn.array_length(Citation.tokens, 1)==len(tokens),
        Citation.tokens.contains(tokens),

    )


def test_tokens(corpus_index, add_doc, add_text):

    """
    Citations should include the set of matching query tokens.
    """

    docs = [
        add_doc(content='Title, David William McClure'),
        add_doc(content='Title, David'),
        add_doc(content='Title, William'),
        add_doc(content='Title, McClure'),
        add_doc(content='Title, David William'),
        add_doc(content='Title, David McClure'),
    ]

    Document_Text.es_insert()

    text = add_text(title='Title', authors=['David William McClure'])
    text_to_docs(text.id)

    for doc in docs:

        tokens = tokenize_field(doc.syllabus.text)

        assert Citation.select().where(

            Citation.text==text,
            Citation.document==doc,

            fn.array_length(Citation.tokens, 1)==len(tokens),
            Citation.tokens.contains(tokens),

        )
