

import threading

from osp.corpus.jobs.read_text import queue_read_text
from flask import Flask, Blueprint, request


corpus = Blueprint('corpus', __name__)


@corpus.route('/text', methods=['POST'])
def test():

    s1 = int(request.args['s1'])
    s2 = int(request.args['s2'])

    spooler = threading.Thread(
        target=queue_read_text,
        args=(s1, s2)
    )

    spooler.start()
    code = 200 if spooler.is_alive() else 500

    return ('', code)
