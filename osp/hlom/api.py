

from osp.common.config import config
from osp.hlom.jobs.hlom_to_docs import hlom_to_docs
from flask import Flask, Blueprint, request
from rq import Queue


hlom = Blueprint('hlom', __name__)


@hlom.route('/query', methods=['POST'])
def query():

    o1 = int(request.form['o1'])
    o2 = int(request.form['o2'])
    job = config.rq.enqueue(meta_job, o1, o2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)


def meta_job(o1, o2):

    """
    Queue HLOM query tasks in the worker.

    Args:
        o1 (int): The first id.
        o2 (int): The second id.
    """

    for i in range(o1, o2+1):
        config.rq.enqueue(hlom_to_docs, i)
