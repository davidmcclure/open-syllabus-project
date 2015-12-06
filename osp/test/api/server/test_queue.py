

from osp.corpus.models import Document
from osp.corpus.jobs import ext_text
from osp.common.utils import partitions


def test_queue(models, api_client, queue):

    """
    /queue should queue a work order.
    """

    # Insert 1000 docs.
    for i in range(1000):
        Document.create(path=str(i))

    api_client.get('/queue', data={
        'model':    'osp.corpus.models.Document',
        'job':      'osp.corpus.jobs.ext_text',
        'index':    5,
        'count':    10,
    })

    # Should queue meta-job.
    assert queue.count == 1

    # Get the id range.
    (id1, id2) = partitions(1, Document.max_id(), 10)[5]

    # Run the queue-job.
    meta = queue.dequeue()
    meta.perform()

    # Should spool work jobs.
    assert queue.count == id2-id1+1

    for i, doc_id in enumerate(range(id1, i2+1)):
        assert queue.jobs[i].func == ext_text
        assert queue.jobs[i].args == (doc_id,)
