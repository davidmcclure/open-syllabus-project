

import os
import importlib

from osp.common.utils import partitions
from osp.hlom.api import hlom
from osp.corpus.api import corpus

from flask import Flask
from rq_dashboard import RQDashboard
from pydoc import locate


# RQ dashboard:
app = Flask(__name__)
RQDashboard(app)


# OSP endpoints:
app.register_blueprint(corpus, url_prefix='/corpus')
app.register_blueprint(hlom, url_prefix='/hlom')


@app.route('/ping')
def ping():
    return ('pong', 200)


@app.route('/queue', methods=['POST'])
def queue():

    """
    Queue a work order.
    """

    # Get model / job callables.
    model = locate(request.form['model'])
    job = locate(request.form['job'])

    # Get worker index and count.
    count = int(request.form['count'])
    index = int(request.form['index'])

    # Get id range.
    (id1, id2) = partitions(1, model.max_id(), count)[index]

    # Meta-job to spool the order.
    def _meta(id1, id2):
        for idx in range(id1, id2+1):
            config.rq.enqueue(job, idx)

    # Queue the meta-job.
    job = config.rq.enqueue(_meta, id1, id2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', code)


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))
