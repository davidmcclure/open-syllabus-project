

import os

from flask import Flask
from rq_dashboard import RQDashboard
from osp.corpus.api import blueprint as corpus


# RQ dashboard:
app = Flask(__name__)
RQDashboard(app)


# OSP REST APIs:
app.register_blueprint(corpus, url_prefix='/corpus')


if __name__ == '__main__':
    app.run()
