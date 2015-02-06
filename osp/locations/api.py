

from osp.common.models.base import redis
from osp.locations.jobs.locate import queue_locate
from flask import Flask, Blueprint, request
from rq import Queue


locations = Blueprint('locations', __name__)


@locations.route('/locate', methods=['POST'])
def query():

    o1 = int(request.args['o1'])
    o2 = int(request.args['o2'])

    queue = Queue(connection=redis)
    job = queue.enqueue(queue_locate, o1, o2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)
