

from osp.common.models.base import redis
from osp.corpus.jobs.read_text import queue_read_text
from flask import Flask, Blueprint, request
from rq import Queue


corpus = Blueprint('corpus', __name__)


@corpus.route('/text', methods=['POST'])
def text():

    o1 = int(request.args['o1'])
    o2 = int(request.args['o2'])

    queue = Queue(connection=redis)
    job = queue.enqueue(queue_read_text, o1, o2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)
