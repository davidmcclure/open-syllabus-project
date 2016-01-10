

import os

from flask import Flask, request, render_template, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from osp.citations.models import Text
from osp.www import utils
from osp.www.cache import cache
from osp.www.hit import Hit


app = Flask(__name__)
cache.init_app(app)


@app.route('/')
def home():

    """
    Home page + ranking interface.
    """

    return render_template(
        'home.html',
        facets=utils.bootstrap_facets(),
    )


@app.route('/api/ranks')
@use_args(dict(

    query           = fields.Str(missing=None),
    size            = fields.Int(missing=200),

    corpus          = fields.List(fields.Str(), missing=None),
    field_id        = fields.List(fields.Int(), missing=None),
    subfield_id     = fields.List(fields.Int(), missing=None),
    institution_id  = fields.List(fields.Int(), missing=None),
    state           = fields.List(fields.Str(), missing=None),
    country         = fields.List(fields.Str(), missing=None),

))
def api_ranks(args):

    """
    Ranking API.
    """

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


@app.route('/text/<corpus>/<identifier>')
def text(corpus, identifier):

    """
    Text profile pages.
    """

    text = Text.get(
        Text.corpus==corpus,
        Text.identifier==identifier,
    )

    # Assigned-with list.
    siblings = utils.assigned_with(text.id)

    # Text metrics.
    count = utils.text_count(text.id)
    score = utils.text_score(text.id)
    color = utils.text_color(score)

    return render_template(
        'text.html',
        text=text,
        siblings=siblings,
        count=count,
        score=score,
        color=color,
        Hit=Hit,
    )


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=os.getenv('PORT', 5000),
        debug=True,
    )
