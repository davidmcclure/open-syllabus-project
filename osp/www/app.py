

import os

from osp.www import utils
from flask import Flask, request, render_template, jsonify

from webargs.flaskparser import use_args
from webargs import fields


app = Flask(__name__)


@app.route('/')
def home():

    return render_template(
        'home.html',
        facets=utils.bootstrap_facets(),
    )


@app.route('/api/ranks')
@use_args(dict(

    query           = fields.Str(missing=None),
    size            = fields.Int(missing=100),

    corpus          = fields.List(fields.Str(), missing=None),
    field_id        = fields.List(fields.Int(), missing=None),
    subfield_id     = fields.List(fields.Int(), missing=None),
    institution_id  = fields.List(fields.Int(), missing=None),
    state           = fields.List(fields.Str(), missing=None),
    country         = fields.List(fields.Str(), missing=None),

))
def ranks(args):

    filters = {f: args[f] for f in [
        'corpus',
        'field_id',
        'subfield_id',
        'institution_id',
        'state',
        'country',
    ]}

    results = utils.rank_texts(
        filters=filters,
        query=args['query'],
        size=args['size'],
    )

    return jsonify(**results)


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=os.getenv('PORT', 5000),
        debug=True,
    )
