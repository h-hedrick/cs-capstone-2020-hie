from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import yaml

#flask app, the application as an object
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #suppress warnings
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@IPAddress/databaseName"

# yaml file will hold sql or sensitive data, local machine only
yam = yaml.load(open('db.yaml'))

db = SQLAlchemy(app) #bind database to app

# route is url direction, so www.thing.com</your route here>
# methods defines what kind of requests the browser can make to the route
@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		some_json = request.get_json()
		# returns a json object with a custom error code of 201
		return jsonify({'you sent' : some_json}), 201
	else:
		return jsonify({"about": "Hello, World!"})

# routes can also hold the variables needed for a request
@app.route('/multi/<int:num>', methods=['GET'])
def get_multiply10(num):
	return jsonify({'result': num*10})

@app.route("/formEX", methods=['GET', 'POST'])
def form():
	if request.method == 'POST':
		# POST, therefore data sent as JSON from form
		formData = request.form
		name = formData['name'] # same key as in html form
		email = formData['email']
		# sql stuff here
		return '<h1> Success! </h1>'
		# alternatively, you can redirect to a different page
		# return redirect(url_for("home"))
	return render_template('index.html')

#sql alchemy
#create a table for the database
class User(db.Model):
	id =  db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	email = db.Column(db.String(120))
	date_created = db.Column(db.DateTime, default=datetime.now)

@app.route('/sql/<name>/<email>')
def sqlAdd(name, email):
	# code for adding entry to table User
	user = User(name=name, email=email)
	db.session.add(user)
	db.session.commit() # changes will not remain unless committed
	return '<h1> Success! </h1>'
if __name__ == '__main__':
	app.run(debug=True) #sets server to update with edits.