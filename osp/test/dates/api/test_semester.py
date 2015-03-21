

from osp.dates.jobs.ext_semester import ext_semester


def test_semester(api_client, queue):

    """
    /semester should queue the semester extraction jobs.
    """

    api_client.post('/dates/semester', data={'o1':1, 'o2':5})
    assert queue.count == 1

    # Run the meta-job.
    meta = queue.dequeue()
    meta.perform()
    assert queue.count == 5

    # Should queue the parsing jobs.
    for i, job in enumerate(queue.jobs):
        assert job.func == ext_semester
        assert job.args == (i+1,)
