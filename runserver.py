from hieapp import app
from hieapp.dbcore import db
from hieapp.models.students import *

def runServer():
	app.run(host='127.0.0.1', port=5000, debug=True) #localhost
	# TODO: set host and port to GCP in config file when ready


# TODO: https://github.com/shea256/angular-flask/blob/master/manage.py
def main():
	# print("Building database: {}".format(yam['mysql_db']))
	init_model()
	print("Database Built, surprisingly")
	# CSV Calls
	# print("Database Populated")

def init_model():
	"""Initializes the database and database tables with relationships"""
	'''
	create database
		if the database doesnt exist, does the URI fail?
		can I use this init to create the database?
	call method to create each table + relations
	commit

	'''
	db.drop_all()
	db.create_all()
	db.session.commit()

	Students.createStudent(9876, "M", False, False, "White", None, "SCOPE", "DGLOS", "-1", False, False, "Georgetown", "USA", "Summer", 2017, True, "fall", 2016, False, "spring", 2020)

if __name__ == '__main__':
	# main()
	runServer()