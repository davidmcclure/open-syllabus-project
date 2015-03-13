

from osp.dates.jobs.ext_file_metadata import ext_file_metadata


def test_semester(api_client, queue):

    """
    The /file-metadata endpoint should queue the meta-job that queues the
    individual file metadata extraction jobs.
    """

    api_client.post('/dates/file-metadata', data={'o1':1, 'o2':5})
    assert queue.count == 1

    # Run the meta-job.
    meta = queue.dequeue()
    meta.perform()
    assert queue.count == 5

    # Should queue the parsing jobs.
    for i, job in enumerate(queue.jobs):
        assert job.func == ext_file_metadata
        assert job.args == (i+1,)
