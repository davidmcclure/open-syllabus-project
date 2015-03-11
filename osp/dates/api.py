

from osp.common.models.base import queue
from osp.dates.jobs.ext_archive_url import ext_archive_url
from flask import Flask, Blueprint, request


dates = Blueprint('dates', __name__)


@dates.route('/archive-url', methods=['POST'])
def archive_url():

    o1 = int(request.form['o1'])
    o2 = int(request.form['o2'])
    job = queue.enqueue(queue_archive_url, o1, o2)

    code = 200 if job.is_queued else 500
    return ('', 200)


def queue_archive_url(o1, o2):

    """
    Queue archive URL parsing tasks in the worker.

    Args:
        o1 (int): The first id.
        o2 (int): The second id.
    """

    for i in range(o1, o2+1):
        queue.enqueue(ext_archive_url, i)
