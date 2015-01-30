

from osp.common.models.base import redis
from osp.citations.hlom.jobs.query import queue_queries
from flask import Flask, Blueprint, request
from rq import Queue


corpus = Blueprint('hlom', __name__)


@corpus.route('/query', methods=['POST'])
def test():

    id1 = int(request.args['id1'])
    id2 = int(request.args['id2'])

    queue = Queue(connection=redis)
    job = queue.enqueue(queue_queries, id1, id2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)
