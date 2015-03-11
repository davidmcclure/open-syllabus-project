

from osp.corpus.jobs.ext_text import ext_text


def test_text(api_client, queue):

    """
    The /text endpoint should queue the job that then queues the individual
    text extraction jobs for each document.
    """

    # Should queue the meta-job.
    api_client.post('/corpus/text', data={'o1':1, 'o2':5})
    assert queue.count == 1

    # Run the meta-job.
    meta = queue.dequeue()
    meta.perform()
    assert queue.count == 5

    # Should queue the text jobs.
    for i, job in enumerate(queue.jobs):
        assert job.func == ext_text
        assert job.args == (i+1,)
