

from osp.corpus.api import queue_text
from osp.corpus.jobs.text import text


def test_queue_text(queue):

    """
    queue_text() should queue text extraction jobs.
    """

    queue_text(1, 5)
    assert queue.count == 5

    for i, job in enumerate(queue.jobs):
        assert job.func == text
        assert job.args == (i+1,)
