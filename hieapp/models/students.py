from hieapp.dbcore import db
from hieapp import app
from hieapp.models.demographics import *
from hieapp.models.enrollments import *
from hieapp.models.high_impact_experiences import *

class Students(db.Model):
	"""Table definition of the Students table. Takes/builds off of base database Model. Acts
	as the root parent of the database.

	__init__(self, id)

	createStudent() -- creates new entry in the Race table, will call __init__
	TODO: searches and documentation
	saveToDB() -- adds and commits instance to database
	"""
	__tablename__ = "students"
	su_id = db.Column(db.Integer, primary_key=True)
	demographic_id = db.relationship("Demographics", backref='students.demographic_id', lazy=True)
	hie_id = db.relationship("HighImpactExpierences", backref='students.hie_id', lazy=True)
	enrollment_id = db.relationship("Enrollments", backref='students.enrollment_id', lazy=True)

	def __init__(self, id):
		self.su_id = id

	# ToString method
	def __repr__(self):
		return "[STUDENTS:SU_id={}, Demographic={}, HIE_Taken={}, Enrollment_Status={}]".format(
			self.su_id, self.demographic_id, self.hie_id, self.enrollment_id)
	
	@classmethod
	def createStudent(cls, su_id, sex, pell_flag, first_gen_flag, first_race, second_race, 
		hie_type, hie_name, hie_course_number, london_flag, dc_flag, city_name, country_name, hie_term, hie_year, 
		fys_flag, fys_aes_term, fys_aes_year, graduated, grad_term, grad_year):
		"""Create a new entry in the Students table and returns the new instance. Extra attributes used for search/finding
		entries in child tables, Demographics and Races.

		Parameters:
		Basic:
			su_id (int) -- Unique student ID number
		Demographic Data:
			sex (char) -- Biological sex ('M' or 'F')
			pell (bool) -- Flag indicating if entry received Pell Grant
			first_gen (bool) -- Flag indicating if entry is a first generation college student
		Race Data:
			first_race (str) -- first race of entry (default None)
			second_race (str) -- second race of entry (default None)
		"""
		print("createStudent: Start")
		newEntry = cls(su_id) # call default constructor

		## Append Demographic Relationship ##
		demoEntry = Demographics.searchForDemographic(su_id=su_id)
		if demoEntry is None:
			print("createStudent: demographic not found, creating new entry")
			demoEntry = Demographics.createDemographic(sex, pell_flag, first_gen_flag, first_race, second_race)
		else:
			print("createStudent: demographic found, using exisiting entry")
		newEntry.demographic_id.append(demoEntry)
		## End Demographic ##

		## Append High Impact Experience Relationship ##
		hieEntry = HighImpactExpierences.searchForHIE(su_id=su_id)
		if hieEntry is None:
			print("createStudent: no HIE entry found, creating new entry")
			hieEntry = HighImpactExpierences.createHIE(hie_type, hie_name, hie_course_number, london_flag, dc_flag, city_name, country_name, hie_term, hie_year)
		else:
			print("createStudent: HIE entry found, using existing entry")
		newEntry.hie_id.append(hieEntry)
		## End HIE ##

		## Append Enrollment Relationship ##
		enrollEntry = Enrollments.searchForEnrollment(su_id=su_id)
		if enrollEntry is None:
			print("createStudent: no Enrollment found, creating new entry")
			enrollEntry = Enrollments.createEnrollment(fys_flag, fys_aes_term, fys_aes_year, graduated, grad_term, grad_year)
		else:
			print("createStudent: enrollment entry found, using existing entry")
		newEntry.enrollment_id.append(enrollEntry)
		## End Enrollment ##

		newEntry.saveToDB()
		print("createStudent: Success! Student entry added to table")
		return newEntry

	#TODO: makes searches

	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

""" code is taken from angular-flask example here: https://github.com/shea256/angular-flask
	comments show this is for angular routing, keeping here just in case
"""