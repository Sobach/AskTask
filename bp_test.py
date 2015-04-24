# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

test_page = Blueprint('test_page', __name__,
                      template_folder='templates',
                      url_prefix='/test')

@test_page.route('/')
def show():
    return 'This is a test Blueprint'