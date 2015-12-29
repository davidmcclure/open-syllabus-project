

import os

from flask import Flask


app = Flask(__name__)


@app.route('/ping')
def ping():
    return ('web', 200)


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=os.getenv('PORT', 5000),
        debug=True,
    )
