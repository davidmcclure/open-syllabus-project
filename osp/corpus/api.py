

import threading

from osp.common.models.base import redis
from osp.corpus.corpus import Corpus
from osp.corpus.jobs.read_text import read_text
from flask import Flask, Blueprint, request
from rq import Queue


corpus = Blueprint('corpus', __name__)


def queue_read_text(s1, s2):

    """
    Queue text extraction tasks in the worker.

    :param s1: The first segment.
    :param s2: The last segment.
    """

    queue = Queue(connection=redis)

    for syllabus in Corpus.from_env(s1=s1, s2=s2).syllabi():
        queue.enqueue(read_text, syllabus.path)


@corpus.route('/text', methods=['POST'])
def test():

    s1 = int(request.args['s1'])
    s2 = int(request.args['s2'])

    spooler = threading.Thread(target=queue_read_text, args=(s1, s2))
    spooler.start()

    code = 200 if spooler.is_alive() else 500
    return ('', code)
