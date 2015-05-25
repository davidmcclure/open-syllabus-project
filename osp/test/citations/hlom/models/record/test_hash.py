

from osp.citations.hlom.models.record import HLOM_Record


def test_ignore_capitalization(add_hlom):

    hashes = set()

    hashes.add(add_hlom('Anna Karenina', 'Leo Tolstoy').hash)
    hashes.add(add_hlom('anna karenina', 'leo tolstoy').hash)
    hashes.add(add_hlom('ANNA KARENINA', 'LEO TOLSTOY').hash)

    assert len(hashes) == 1


def test_ignore_whitespace(add_hlom):

    hashes = set()

    hashes.add(add_hlom('Anna  Karenina', 'Leo  Tolstoy').hash)
    hashes.add(add_hlom(' Anna Karenina ', ' Leo Tolstoy ').hash)

    assert len(hashes) == 1


def test_ignore_punctuation(add_hlom):

    hashes = set()

    hashes.add(add_hlom('Anna Karenina /', 'Leo Tolstoy /').hash)
    hashes.add(add_hlom('Anna Karenina.', 'Leo Tolstoy.').hash)
    hashes.add(add_hlom('"Anna Karenina,"', 'Leo Tolstoy').hash)

    assert len(hashes) == 1


def test_ignore_articles(add_hlom):

    hashes = set()

    hashes.add(add_hlom('The Republic', 'Plato').hash)
    hashes.add(add_hlom('A Republic', 'Plato').hash)
    hashes.add(add_hlom('An Republic"', 'Plato').hash)

    assert len(hashes) == 1


def test_ignore_author_order(add_hlom):

    hashes = set()

    hashes.add(add_hlom('Anna Karenina', 'Leo Tolstoy').hash)
    hashes.add(add_hlom('Anna Karenina', 'Tolstoy, Leo').hash)

    assert len(hashes) == 1
