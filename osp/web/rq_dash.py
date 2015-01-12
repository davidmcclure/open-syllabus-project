

import os

from flask import Flask
from rq_dashboard import RQDashboard


app = Flask(__name__)
RQDashboard(app)
app.run(port=os.getenv('RQ_PORT', 5000))
