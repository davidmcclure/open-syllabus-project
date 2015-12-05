

import os

from flask import Flask
from rq_dashboard import RQDashboard
from osp.corpus.api import corpus
from osp.hlom.api import hlom
from osp.dates.api import dates


# RQ dashboard:
app = Flask(__name__)
RQDashboard(app)


# OSP endpoints:
app.register_blueprint(corpus, url_prefix='/corpus')
app.register_blueprint(hlom, url_prefix='/hlom')
app.register_blueprint(dates, url_prefix='/dates')


@app.route('/ping')
def ping():
    return ('pong', 200)


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))
