

import pytest

from osp.common.config import config
from osp.corpus.models import Document
from osp.corpus.jobs import ext_text


pytestmark = pytest.mark.usefixtures('db', 'rq')


def test_queue(api_client):

    """
    /queue should queue a work order.
    """

    for i in range(100):
        Document.create(path=str(i))

    r = api_client.post('/queue', data=dict(

        model_import    = 'osp.corpus.models.Document',
        job_import      = 'osp.corpus.jobs.ext_text',
        worker_count    = 20,
        offset          = 10,

    ))

    # Should queue meta-job.
    assert config.rq.count == 1

    # Run the queue-job.
    meta = config.rq.dequeue()
    meta.perform()

    # Should spool the work jobs.
    for i, doc in enumerate(Document.page_cursor(20, 10)):
        assert config.rq.jobs[i].func == ext_text
        assert config.rq.jobs[i].args == (doc.id,)
