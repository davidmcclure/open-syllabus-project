

from osp.common.config import config
from osp.corpus.jobs.ext_text import ext_text
from flask import Flask, Blueprint, request


corpus = Blueprint('corpus', __name__)


@corpus.route('/text', methods=['POST'])
def text():

    queue = config.get_rq()

    o1 = int(request.form['o1'])
    o2 = int(request.form['o2'])
    job = queue.enqueue(queue_text, o1, o2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)


def queue_text(o1, o2):

    """
    Queue text extraction tasks in the worker.

    Args:
        o1 (int): The first id.
        o2 (int): The second id.
    """

    queue = config.get_rq()

    for i in range(o1, o2+1):
        queue.enqueue(ext_text, i)
