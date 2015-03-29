

from osp.locations.jobs.match_doc import match_doc


def test_text(api_client, queue):

    """
    /match-doc should queue the text extraction jobs.
    """

    # Should queue the meta-job.
    api_client.post('/locations/match-doc', data={'o1':1, 'o2':5})
    assert queue.count == 1

    # Run the meta-job.
    meta = queue.dequeue()
    meta.perform()
    assert queue.count == 5

    # Should queue the text jobs.
    for i, job in enumerate(queue.jobs):
        assert job.func == match_doc
        assert job.args == (i+1,)
