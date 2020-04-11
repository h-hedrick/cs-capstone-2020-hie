# this is where API routes are defined
# can be extended into a larger folder

from flask import Flask, render_template, make_response
from hieapp import app

#TODO: https://github.com/shea256/angular-flask/blob/master/angular_flask/controllers.py
@app.route('/')
@app.route('/login', methods=['GET','POST'])
def basic_pages(**kwargs):
	return make_response(open('hieapp/templates/index.html').read())
	# I think this is where angular gets called?
	# angular call in index.html?

# TODO: other routes if need to be defined here, else angular?

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404