

import threading

from osp.corpus.jobs.read_text import queue
from flask import Flask, Blueprint, request


corpus = Blueprint('corpus', __name__)


@corpus.route('/text', methods=['POST'])
def test():

    s1 = int(request.args['s1'])
    s2 = int(request.args['s2'])
    queue(s1, s2)
    return ('', 200)
