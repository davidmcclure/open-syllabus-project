

from osp.corpus.api import queue_text


def test_text(api_client, queue):

    """
    The /text endpoint should queue the job that then queues the individual
    text extraction jobs for each document.
    """

    api_client.post('/corpus/text', data={'o1':1, 'o2':5})

    assert queue.count == 1
    assert queue.jobs[0].func == queue_text
    assert queue.jobs[0].args == (1, 5)
