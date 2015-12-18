

import pytest
import json

from osp.common.utils import partitions
from osp.common.config import config
from osp.corpus.models import Document
from osp.corpus.jobs import ext_text


@pytest.mark.api
def test_queue(models, api_client):

    """
    /queue should queue a work order.
    """

    # Insert 1000 docs.
    for i in range(1000):
        Document.create(path=str(i))

    r = api_client.post('/queue', data={
        'model':    'osp.corpus.models.Document',
        'job':      'osp.corpus.jobs.ext_text',
        'index':    5,
        'count':    10,
    })

    # Should queue meta-job.
    assert config.rq.count == 1

    # Get the id range.
    (id1, id2) = partitions(1, Document.max_id(), 10)[5]

    # Run the queue-job.
    meta = config.rq.dequeue()
    meta.perform()

    # Should spool the work jobs.
    for i, doc_id in enumerate(range(id1, id2+1)):
        assert config.rq.jobs[i].func == ext_text
        assert config.rq.jobs[i].args == (doc_id,)

    # Should return the id range.
    assert json.loads(r.data.decode('utf8')) == {
        'id1': id1,
        'id2': id2,
    }
