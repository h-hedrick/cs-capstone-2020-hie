"""
	Initialization file for the database.
	Script will define the logical model of the mysql database.
	Then will call other scripts to populate the database with the data
	specifically related to a csv file.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yaml

# Set working directory
setwd = "./sql_scripts/csv_files/"
app = Flask(__name__)
yam = yaml.load(open('db.yaml'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #suppress warnings
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{}:{}@{}/{}".format(
			yam["mysql_user"],
			yam["mysql_password"],
			yam["mysql_host"],
			yam["mysql_db"])
db = SQLAlchemy(app)

def main():
	print("Building database")
	init_model()
def init_model():
	"""Initializes the database and database tables with relationships"""
	'''
	create database
		if the database doesnt exist, does the URI fail?
		can I use this init to create the database?
	call methods to create each table + relations
	commit

	'''

if __name__ == '__main__':
	main()
