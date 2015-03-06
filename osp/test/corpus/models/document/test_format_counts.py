

from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format


def test_format_counts(models):

    """
    Document.format_counts()
    """

    # 1 doc with 'format1'.
    d1 = Document.create(path='000/1')
    f1 = Document_Format.create(document=d1, format='format1')

    # 2 docs with 'format2'.
    d2 = Document.create(path='000/2')
    f2 = Document_Format.create(document=d2, format='format2')
    d3 = Document.create(path='000/3')
    f3 = Document_Format.create(document=d3, format='format2')

    # 3 docs with 'format3'.
    d4 = Document.create(path='000/4')
    f4 = Document_Format.create(document=d4, format='format3')
    d5 = Document.create(path='000/5')
    f5 = Document_Format.create(document=d5, format='format3')
    d6 = Document.create(path='000/6')
    f6 = Document_Format.create(document=d6, format='format3')

    assert Document_Format.format_counts() == [
        ('format3', 3),
        ('format2', 2),
        ('format1', 1)
    ]
