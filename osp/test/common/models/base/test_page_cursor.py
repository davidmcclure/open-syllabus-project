

from osp.citations.models import Text


def test_page_cursor(add_text):

    """
    BaseModel.page_cursor() should generate record instances in an id-ordered
    "page", defined by a page count and 0-based index.
    """

    for i in range(100):
        add_text()

    ids = []
    for i in range(7):
        ids.append([t.id for t in Text.page_cursor(7, i)])

    # 7 pages:
    assert len(ids) == 7

    # 1-100 range:
    assert sum(ids, []) == list(range(1, 101))
