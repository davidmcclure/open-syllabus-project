

from osp.hlom.jobs import hlom_to_docs


def test_semester(api_client, queue):

    """
    /query should queue HLOM query jobs.
    """

    api_client.post('/hlom/query', data={'o1':1, 'o2':5})
    assert queue.count == 1

    # Run the meta-job.
    meta = queue.dequeue()
    meta.perform()
    assert queue.count == 5

    # Should queue the query jobs.
    for i, job in enumerate(queue.jobs):
        assert job.func == hlom_to_docs
        assert job.args == (i+1,)
