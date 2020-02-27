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
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{}:{}@{}/{}".format(
# 			yam["mysql_user"],
# 			yam["mysql_password"],
# 			yam["mysql_host"],
# 			yam["mysql_db"])
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/Users/Matt/Documents/GitHub/cs-capstone-2020-hie/sql_scripts/testdb.db"
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
	db.drop_all()
	db.create_all()
	db.session.commit()
	test = Terms(term='Spring', year=1997)
	test.saveToDB()
	print(test)

###########################################
# Database Table Model and Relationships  #
###########################################

class Students(db.Model):
	__tablename__ = "students"
	su_id = db.Column(db.Integer, primary_key=True)
	demographic_id = db.relationship("Demographics", backref='students', lazy=True)
	hiesTaken = db.relationship("HighImpactExpierences", backref='students', lazy=True)
	enrollment_id = db.relationship("Enrollments", backref='students', lazy=True)

# class HiesStudents(db.Model):
# 	student_id = db.Column(db.Integer, db.ForeignKey("students.su_id"), primary_key=True)
# 	hie_id = db.Column(db.Integer, db.ForeignKey("high_impact_expierences.hie_id"), nullable=False)

class HighImpactExpierences(db.Model):
	__tablename__ = "high_impact_expierences"
	hie_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	hie_type = db.Column(db.String(50), nullable=False)
	hie_course_number = db.Column(db.String(50))
	location_id = db.relationship("Locations", backref='high_impact_expierences', lazy=True)
	term_id = db.relationship("Terms", backref='high_impact_expierences', lazy=True)

class Terms(db.Model):
	__tablename__ = "terms"
	term_id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.String(6))
	year = db.Column(db.Integer, nullable=False)

	# Basically, a toString() method
	def __repr__(self):
		return "[TERMS:id=%d, term=%s, year=%d]".format(self.id, self.term, self.year)

	# init to define/create new entries
	def __init__(self, term, year):
		self.term = term.upper()
		self.year = year
	
	# quick save to DB method
	def saveToDB(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def searchTerms(cls, term):
		id = db.session.query(cls).filter(cls.term == term)
		# if id is NONE:
		# 	# create new term if none exists
		# else:
			# print(type(id))
			# return id

class Locations(db.Model):
	__tablename__ = "locations"
	location_id = db.Column(db.Integer, primary_key=True)
	hie_id = db.Column(db.Integer, db.ForeignKey('high_impact_expierences.hie_id'))
	city_id = db.relationship("Cities", backref="locations", lazy=True)
	country_id = db.relationship("Countries", backref="locations", lazy=True)
	london_flag = db.Column(db.Boolean)
	dc_flag = db.Column(db.Boolean)

class Demographics(db.Model):
	__tablename__ = "demographics"
	demographic_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	pell_flag = db.Column(db.Boolean)
	sex = db.Column(db.String(1), nullable=False)
	race_id = db.relationship("Races", backref='demographics', lazy=True)
	first_gen_flag = db.Column(db.Boolean)

class Races(db.Model):
	__tablename__ = "races"
	race_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	first_race = db.Column(db.String(20), nullable=False)
	second_race = db.Column(db.String(20))

class Enrollments(db.Model):
	__tablename__ = "enrollments"
	enrollment_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	fys_term = db.relationship("Terms", backref='enrollments', lazy=True)
	aes_term = db.relationship("Terms", backref='enrollments', lazy=True)
	graduation_id = db.relationship("GraduationClass", backref='enrollments', lazy=True)
	loa_id = db.relationship("LeaveOfAbsences", backref='enrollments', lazy=True)

class GraduationClasses(db.Model):
	__tablename__ = "graduation_class"
	graduation_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	expected_term = db.relationship("Terms", backref='graduation_class', lazy=True)
	actual_term = db.relationship("Terms", backref='graduation_class', lazy=True)

class LeaveOfAbsences(db.Model):
	__tablename__ = "leave_of_absences"
	loa_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.enrollment_id'))
	start_term = db.relationship("Terms", backref='leave_of_absences', lazy=True)
	end_term = db.relationship("Terms", backref='leave_of_absences', lazy=True)
	loa_description = db.Column(db.Text)

class cities(db.Model):
	__tablename__ = 'cities'
	city_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	country_id = db.relationship('Countries', backref='cities', lazy=True)

class countries(db.Model):
	__tablename__ = 'countries'
	country_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, unique=True, nullable=False)

if __name__ == '__main__':
	main()
