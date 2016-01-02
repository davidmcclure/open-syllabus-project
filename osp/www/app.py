

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


@app.route('/api/ranks')
def ranks():

    query = request.args.get('query')

    # Parse the filter args.
    filters = {f: request.args.get(f) for f in [
        'corpus',
        'field_id',
        'subfield_id',
        'institution_id',
        'state',
        'country',
    ]}

    # 100 docs, by default.
    size = request.args.get('size', 100)

    results = utils.rank_texts(
        query=query,
        filters=filters,
        size=size,
    )

    return jsonify(**results)


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=os.getenv('PORT', 5000),
        debug=True,
    )
