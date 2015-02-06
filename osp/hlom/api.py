

from osp.common.models.base import redis
from osp.citations.hlom.jobs.query import queue_queries
from flask import Flask, Blueprint, request
from rq import Queue


hlom = Blueprint('hlom', __name__)


@hlom.route('/query', methods=['POST'])
def query():

    o1 = int(request.args['o1'])
    o2 = int(request.args['o2'])

    queue = Queue(connection=redis)
    job = queue.enqueue(queue_queries, o1, o2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)
