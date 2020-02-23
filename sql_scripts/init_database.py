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
	print("Building database: {}".format(yam['mysql_db']))
	init_model()
	print("Database Built, surprisingly")

def init_model():
	"""Initializes the database and database tables with relationships"""
	'''
	create database
		if the database doesnt exist, does the URI fail?
		can I use this init to create the database?
	call method to create each table + relations
	commit

	'''
	db.create_all()
	db.session.commit()

###########################################
# Database Table Model and Relationships  #
###########################################

class Students(db.Model):
	#Default tablename = lowercase(class name)
	su_id = db.Column(db.Integer, primary_key=True)
	demographic_id = db.relationship("Demographics", backref='Students', lazy=True)
	hiesTaken = db.relationship("HiesStudents", backref='Students', lazy=True)
	enrollment_id = db.relationship("Enrollments", backref='Students', lazy=True)

class HiesStudents(db.Model):
	student_id = db.Column(db.Integer, db.ForeignKey("students.su_id"), primary_key=True)
	hie_id = db.Column(db.Integer, db.ForeignKey("high_impact_expierences.hie_id"), nullable=False)

class HighImpactExpierences(db.Model):
	hie_id = db.Column(db.Integer, primary_key=True)
	hie_type = db.Column(db.String(50), nullable=False)
	hie_course_number = db.Column(db.String(50))
	location_id = db.relationship("Locations", backref='HighImpactExpierences', lazy=True)
	term_id = db.relationship("Terms", backref='HighImpactExpierences', lazy=True)

class Terms(db.Model):
	term_id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.String(6))
	year = db.Column(db.Integer, nullable=False)

class Locations(db.Model):
	location_id = db.Column(db.Integer, primary_key=True)
	city_id = db.relationship("Cities", backref="Locations", lazy=True)
	country_id = db.relationship("Countries", backref="Locations", lazy=True)
	london_flag = db.Column(db.Boolean)
	dc_flag = db.Column(db.Boolean)

class Demographics(db.Model):
	demographic_id = db.Column(db.Integer, primary_key=True)
	pell_flag = db.Column(db.Boolean)
	sex = db.Column(db.String(1), nullable=False)
	race_id = db.relationship("Races", backref='Demographics', lazy=True)
	first_gen_flag = db.Column(db.Boolean)

class Races(db.Model):
	race_id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	first_race = db.Column(db.String(20), nullable=False)
	second_race = db.Column(db.String(20))

class Enrollments(db.Model):
	enrollment_id = db.Column(db.Integer, primary_key=True)
	fys_term = db.relationship("Terms", backref='Enrollments', lazy=True)
	aes_term = db.relationship("Terms", backref='Enrollments', lazy=True)
	graduation_id = db.relationship("GraduationClasses", backref='Enrollments', lazy=True)
	loa_id = db.relationship("LeaveOfAbsences", backref='Enrollments', lazy=True)

class GraduationClasses(db.Model):
	graduation_id = db.Column(db.Integer, primary_key=True)
	expected_term = db.relationship("Terms", backref='GraduationClasses', lazy=True)
	actual_term = db.relationship("Terms", backref='GraduationClasses', lazy=True)

class LeaveOfAbsences(db.Model):
	loa_id = db.Column(db.Integer, primary_key=True)
	start_term = db.relationship("Terms", backref='LeaveOfAbsences', lazy=True)
	end_term = db.relationship("Terms", backref='LeaveOfAbsences', lazy=True)
	loa_description = db.Column(db.Text)

if __name__ == '__main__':
	main()
