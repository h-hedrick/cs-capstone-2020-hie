from hieapp import app
from hieapp.dbcore import db

from hieapp.models.students import *

def runServer():
	"""Runs the Flask app, creating server and accepting requests."""
	app.run(host='127.0.0.1', port=5000, debug=True) #localhost
	# TODO: set host and port to GCP in config file when ready

# TODO: https://github.com/shea256/angular-flask/blob/master/manage.py
def main():
	init_model()
	#TODO: CSV script Calls
	runServer()

def init_model():
	"""Initializes the database and database tables with relationships"""
	db.drop_all()
	db.create_all()
	db.session.commit()

	# Example student data being added to the database
	Students.createStudent(9876, "M", False, False, "White", None, "SCOPE", "DGLOS", "-1", False, False, "Georgetown", "USA", "Summer", 2017, True, "fall", 2016, False, "spring", 2020)

if __name__ == '__main__':
	main()