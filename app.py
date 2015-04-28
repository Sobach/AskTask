# -*- coding: utf-8 -*-

from flask import Flask
import flask_sijax
from bp_builder import q_builder

app = Flask(__name__)
app.register_blueprint(q_builder)
flask_sijax.Sijax(app)
app.run(debug=True, port=5000, host = 'localhost')