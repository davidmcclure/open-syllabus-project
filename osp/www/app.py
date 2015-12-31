

import os

from osp.www import utils
from flask import Flask, request, render_template, jsonify


app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'home.html',
        facets=utils.bootstrap_facets(),
    )


# TODO
@app.route('/api/ranks')
def ranks():
    return jsonify(results=utils.rank_texts())


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=os.getenv('PORT', 5000),
        debug=True,
    )
