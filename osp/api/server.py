

import os

from osp.common.config import config
from osp.common.utils import partitions

from flask import Flask, request
from rq_dashboard import RQDashboard
from pydoc import locate


# RQ dashboard:
app = Flask(__name__)
RQDashboard(app)


@app.route('/ping')
def ping():
    return ('pong', 200)


@app.route('/queue', methods=['POST'])
def queue():

    """
    Queue a work order.
    """

    config.rq.enqueue(
        queue_page,
        request.form['model_import'],
        request.form['job_import'],
        int(request.form['worker_count']),
        int(request.form['offset']),
        timeout=3600,
    )

    return ('', 200)


def queue_page(model_import, job_import, worker_count, offset):

    """
    Spool a page of model instances for a job.

    Args:
        model_import (str): The model class import string.
        job_import (str): The job import string.
        worker_count (int): The total number of workers.
        offset (int): A 0-based index for this worker.
    """

    # Import callables.
    model = locate(model_import)
    job = locate(job_import)

    for row in model.page_cursor(worker_count, offset):
        config.rq.enqueue(job, row.id)


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))
