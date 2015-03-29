

from osp.common.config import config
from osp.locations.jobs.match_doc import match_doc
from flask import Flask, Blueprint, request


locations = Blueprint('locations', __name__)


@locations.route('/match-doc', methods=['POST'])
def text():

    o1 = int(request.form['o1'])
    o2 = int(request.form['o2'])
    job = config.rq.enqueue(meta_match_doc, o1, o2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)


def meta_match_doc(o1, o2):

    """
    Queue doc -> inst matching tasks in the worker.

    Args:
        o1 (int): The first id.
        o2 (int): The second id.
    """

    for i in range(o1, o2+1):
        config.rq.enqueue(match_doc, i)
