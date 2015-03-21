

from osp.dates.jobs.ext_archive_url import ext_archive_url


def test_archive_url(api_client, queue):

    """
    /archive-url should queue the archive URL extraction jobs.
    """

    api_client.post('/dates/archive-url', data={'o1':1, 'o2':5})
    assert queue.count == 1

    # Run the meta-job.
    meta = queue.dequeue()
    meta.perform()
    assert queue.count == 5

    # Should queue the parsing jobs.
    for i, job in enumerate(queue.jobs):
        assert job.func == ext_archive_url
        assert job.args == (i+1,)
