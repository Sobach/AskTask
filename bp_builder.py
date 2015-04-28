# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
import flask_sijax
import md5, datetime, json
from pymongo import MongoClient
from bs4 import BeautifulSoup
q_builder = Blueprint('q_builder', __name__,
                      template_folder='templates',
                      url_prefix='/q_builder')

class BuilderSijax(object):
	@staticmethod
	def add_question(obj_response, w_id, questionnaire, offset):
		q_id = md5.new(str(datetime.datetime.now()) + w_id + questionnaire['id']).hexdigest()
		questionnaire['content'].append({'id':q_id})
		element, jscode = render_element(q_id, w_id)
		code = '''window.questionnaire = {};
		var i=0; 
		$("div.layout").children("div").each(function()
		{{
			if($(this).offset().top>={})
			{{
				$('{}').insertBefore($(this));
				i=1;
				return false; 
			}}
		}})
		if(i!=1)
		{{
			$("div.layout").append('{}');
		}}
		$("div#{}").accordion({{ header: "h3", collapsible: true }});\n{}
		'''.format(json.dumps(questionnaire), offset, element, element, q_id, jscode)
		obj_response.script(code)

@q_builder.route('/', methods=['GET', 'POST'])
def show(q_id='f128ab62d27f99ef2cc9b451c7d1bce1'):
	if g.sijax.is_sijax_request:
		g.sijax.register_object(BuilderSijax)
		return g.sijax.process_request()
	client = MongoClient('localhost', 27017)
	questionnaire = client.asktask.questionnaries.find_one({'id':q_id})
	questionnaire.pop("_id", None)
	return render_template('builder.html', page = {'title':'My first page', 'description':'My page'}, widgets = widgets(), questionnaire = questionnaire)

def widgets(w_id = None):
	client = MongoClient('localhost', 27017)
	if not w_id:
		return [x for x in client.asktask.q_builder_widgets.find()]
	else:
		return client.asktask.q_builder_widgets.find_one({'id':w_id})

def render_element(e_id, e_type):
	client = MongoClient('localhost', 27017)
	widget = client.asktask.q_builder_widgets.find_one({'id':e_type})
	code_js = ''
	code_block = BeautifulSoup('<div class="quest_element" id="{}"></div>'.format(e_id))
	code_block.div.append(code_block.new_tag('h3'))
	code_block.div.h3.append(code_block.new_tag('i', **{'class':'fa fa-{}'.format(widget['icon'])}))
	code_block.div.h3.append('&nbsp;'+widget['title'])
	code_block.div.append(code_block.new_tag('div'))
	#code_block.div.div.append(code_block.new_tag('p'))
	#code_block.div.div.p.append(widget['description'])
	if 'form' in widget:
		form = code_block.new_tag('form', **{'class':'widget_settings pure-form'})
		for field in widget['form']:
			if field['type'] == 'textarea':
				form.append(code_block.new_tag('textarea', **{'placeholder':field['name']}))
			elif field['type'] == 'select':
				sel_el = code_block.new_tag('select')
				for opt in field['options']:
					o = code_block.new_tag('option')
					o.append(opt)
					sel_el.append(o)
				form.append(sel_el)
			elif field['type'] == 'spinner':
				form.append(code_block.new_tag('input', **{'class':'spinner','id':'{}-{}'.format(e_id, field['id']), 'value':field['value']}))
				js_opt = []
				if 'min' in field.keys():
					js_opt.append('min: {}'.format(field['min']))
				if 'max' in field.keys():
					js_opt.append('max: {}'.format(field['max']))
				code_js += '$( "#{}-{}" ).spinner({{\n'.format(e_id, field['id'])
				code_js += ',\n'.join(js_opt)
				code_js += '});\n'
			else:
				field['id'] = '{}-{}'.format(e_id, field['id'])
				form.append(code_block.new_tag('input', **{k:v for k,v in field.items()}))
		code_block.div.div.append(form)
	return code_block.encode_contents(formatter=None), code_js