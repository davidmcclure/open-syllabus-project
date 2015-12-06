

import os
import importlib

from flask import Flask
from rq_dashboard import RQDashboard
from osp.corpus.api import corpus
from osp.hlom.api import hlom


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
    pass # TODO


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))
