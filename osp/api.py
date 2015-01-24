

import os

from flask import Flask
from rq_dashboard import RQDashboard
from osp.corpus.api import corpus


# RQ dashboard:
app = Flask(__name__)
RQDashboard(app)


# OSP REST APIs:
app.register_blueprint(corpus, url_prefix='/corpus')


@app.route('/ping')
def ping():
    return 'pong'


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))
