

from osp.common.models.base import redis
from osp.corpus.jobs.read_text import queue_read_text
from flask import Flask, Blueprint, request
from rq import Queue


corpus = Blueprint('corpus', __name__)


@corpus.route('/text', methods=['POST'])
def test():

    s1 = int(request.args['s1'])
    s2 = int(request.args['s2'])

    queue = Queue(connection=redis)
    job = queue.enqueue(queue_read_text, s1, s2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)
