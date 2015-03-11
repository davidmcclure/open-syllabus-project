

from osp.dates.jobs.archive_url import archive_url


def test_text(api_client, queue):

    """
    The /archive-url endpoint should queue the meta-job that queues the
    individual archive ULR extraction jobs.
    """

    pass
