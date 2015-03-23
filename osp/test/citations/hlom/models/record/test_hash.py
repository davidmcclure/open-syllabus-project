

from osp.citations.hlom.models.record import HLOM_Record


def test_hash(models, add_hlom):

    hashes = set()

    # Ignore capitalization.
    hashes.add(add_hlom('Anna Karenina', 'Leo Tolstoy').hash)
    hashes.add(add_hlom('anna karenina', 'leo tolstoy').hash)
    hashes.add(add_hlom('ANNA KARENINA', 'LEO TOLSTOY').hash)

    # Ignore whitespace.
    hashes.add(add_hlom('Anna  Karenina', 'Leo  Tolstoy').hash)
    hashes.add(add_hlom(' Anna Karenina ', ' Leo Tolstoy ').hash)

    # Ignore punctuation.
    hashes.add(add_hlom('Anna Karenina /', 'Leo Tolstoy /').hash)
    hashes.add(add_hlom('Anna Karenina.', 'Leo Tolstoy.').hash)
    hashes.add(add_hlom('"Anna Karenina,"', 'Leo Tolstoy').hash)

    assert len(hashes) == 1

