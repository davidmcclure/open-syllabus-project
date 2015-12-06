

from osp.corpus.models import Document


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

    # Should queue the meta-job.
    assert queue.count == 1

    # run meta-job
    # should queue jobs
    # check func/args
    # should return id range
