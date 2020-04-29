# this is where API routes are defined
# can be extended into a larger folder

from flask import Flask, jsonify, request, render_template, make_response
from hieapp import app
from hieapp.dbcore import db
from hieapp.entities import *

#TODO: https://github.com/shea256/angular-flask/blob/master/angular_flask/controllers.py
@app.route('/')
@app.route('/login', methods=['GET','POST'])
def basic_pages(**kwargs):
	return make_response(open('hieapp/templates/index.html').read())
	# I think this is where angular gets called
	# angular call to index.html --> after that, angular routing(?)

# TODO: other routes if need to be defined here, else angular? ask alice

@app.route('/home')
@app.route('/home/default', methods=['GET']) #methods for anular to call
def getDefaultData():

	#get data from db
	data = db.session.query() #TODO QUERY

	#transform data into json using entity
	schema = studentEntity(many=True)
	res = schema.dump(data)

	return jsonify(res.data)

@app.errorhandler(404)
def page_not_found(e):
	#TODO: make 404 template
	return render_template('templates/404.html'), 404