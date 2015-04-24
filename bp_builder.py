# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from pymongo import MongoClient
q_builder = Blueprint('q_builder', __name__,
                      template_folder='templates',
                      url_prefix='/q_builder')

def widgets():
	client = MongoClient('localhost', 27017)
	return [x for x in client.asktask.q_builder_widgets.find()]

@q_builder.route('/')
def show():
	#widgets = widgets()
	return render_template('builder.html', page = {'title':'My first page', 'description':'My page'}, widgets = widgets())