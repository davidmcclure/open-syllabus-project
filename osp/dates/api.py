

from osp.common.models.base import queue
from osp.dates.jobs.ext_archive_url import ext_archive_url
from osp.dates.jobs.ext_semester import ext_semester
from osp.dates.jobs.ext_file_metadata import ext_file_metadata
from flask import Flask, Blueprint, request


dates = Blueprint('dates', __name__)


@dates.route('/archive-url', methods=['POST'])
def archive_url():

    o1 = int(request.form['o1'])
    o2 = int(request.form['o2'])
    job = queue.enqueue(queue_jobs, ext_archive_url, o1, o2)

    code = 200 if job.is_queued else 500
    return ('', 200)


@dates.route('/semester', methods=['POST'])
def semester():

    o1 = int(request.form['o1'])
    o2 = int(request.form['o2'])
    job = queue.enqueue(queue_jobs, ext_semester, o1, o2)

    code = 200 if job.is_queued else 500
    return ('', 200)


@dates.route('/file-metadata', methods=['POST'])
def file_metadata():

    o1 = int(request.form['o1'])
    o2 = int(request.form['o2'])
    job = queue.enqueue(queue_jobs, ext_file_metadata, o1, o2)

    code = 200 if job.is_queued else 500
    return ('', 200)


def queue_jobs(job, o1, o2):

    """
    Queue archive URL parsing tasks in the worker.

    Args:
        job (function): The job.
        o1 (int): The first id.
        o2 (int): The second id.
    """

    for i in range(o1, o2+1):
        queue.enqueue(job, i)
