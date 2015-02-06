

import os

from flask import Flask
from rq_dashboard import RQDashboard
from osp.corpus.api import corpus
from osp.citations.hlom.api import hlom
from osp.locations.api import locations


# RQ dashboard:
app = Flask(__name__)
RQDashboard(app)


# OSP REST APIs:
app.register_blueprint(corpus, url_prefix='/corpus')
app.register_blueprint(hlom, url_prefix='/hlom')
app.register_blueprint(locations, url_prefix='/locations')


@app.route('/ping')
def ping():
    return 'pong'


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))
