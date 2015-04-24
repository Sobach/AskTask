# -*- coding: utf-8 -*-

from flask import Flask
from bp_builder import q_builder

app = Flask(__name__)
app.register_blueprint(q_builder)
app.run(debug=True, port=5000, host = 'localhost')