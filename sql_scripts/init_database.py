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

	# #test adding to multiple relation tables
	# stu = Students('12345')
	# hie = HighImpactExpierences(stu.su_id, 'SCOPE', 'CSC200')
	# hie.location_id = 

	Students.createStudent(9876, "M", True, False, "White", None, "SCOPE", "AI with Schrum", "010101", False, False, "Georgetown", "USA", "Summer", 1984, -1)

###########################################
# Database Table Model and Relationships  #
###########################################

termToHIE = db.Table('term_hie',
	db.Column('term_id', db.Integer, db.ForeignKey('terms.term_id')),
	db.Column('hie_id', db.Integer, db.ForeignKey('high_impact_expierences.hie_id'))
)

termToGrad = db.Table('term_grad',
	db.Column('term_id', db.Integer, db.ForeignKey('terms.term_id')),
	db.Column('grad_id', db.Integer, db.ForeignKey('graduation_class.graduation_id'))
)

termToEnroll = db.Table('term_enroll',
	db.Column('term_id', db.Integer, db.ForeignKey('terms.term_id')),
	db.Column('enrollment_id', db.Integer, db.ForeignKey('enrollments.enrollment_id'))
)

# termToLoa = db.Table('term_loa',
# 	db.Column('term_id', db.Integer, db.ForeignKey('terms.term_id')),
# 	db.Column('loa_id', db.Integer, db.ForeignKey('leave_of_absences.loa_id'))
# )

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
		hie_type, hie_name, hie_course_number, london_flag, dc_flag, city_name, country_name, term, year, 
		enrollment_id):
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
			hieEntry = HighImpactExpierences.createHIE(hie_type, hie_name, hie_course_number, london_flag, dc_flag, city_name, country_name, term, year)
		else:
			print("createStudent: HIE entry found, using existing entry")
		newEntry.hie_id.append(hieEntry)
		## End HIE ##

		## Append Enrollment Relationship ##
		# newEntry.enrollment_id = None
		## End Enrollment ##

		newEntry.saveToDB()
		print("createStudent: student entry added to table")
		return newEntry

	#TODO: makes searches

	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

class HighImpactExpierences(db.Model):
	__tablename__ = "high_impact_expierences"
	hie_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	hie_type = db.Column(db.String(50), nullable=False)
	hie_name = db.Column(db.String(50))
	hie_course_number = db.Column(db.String(50))
	location_id = db.relationship("Locations", backref='high_impact_expierences.location_id', lazy=True)
	term_id = db.relationship("Terms", secondary=termToHIE, backref='termToHIE.term_id', lazy='dynamic')

	def __init__(self, hie_type, hie_name, hie_course_number):
		self.hie_name = hie_name
		self.hie_type = hie_type
		self.hie_course_number = hie_course_number

	@classmethod
	def createHIE(cls, hie_type, hie_name, hie_course_number, london_flag, dc_flag, city_name, country_name, term, year):
		print("createHIE: Start")
		newEntry = cls(hie_type, hie_name, hie_course_number) # call default constructor

		## Append Location Relationship ##
		locEntry = Locations.searchForLocation(hie_id=newEntry.hie_id)
		if locEntry is None:
			print("createHIE: location not found, creating new entry")
			locEntry = Locations.createLocation(london_flag, dc_flag, city_name, country_name)
		else:
			print("createHIE: location found, using exisiting entry")
		newEntry.location_id.append(locEntry)
		## End Location ##

		## Append Term Relationship ##
		termEntry = Terms.searchForTerm(term=term, year=year)
		if termEntry is None:
			print("createHIE: term not found, creating new entry")
			termEntry = Terms.createTerm(term, year)
		else:
			print("createHIE: term found, using existing entry")
		newEntry.term_id.append(termEntry)
		## End Term ##

		newEntry.saveToDB()
		print("createHIE: HIE entry added to table")
		return newEntry

	@classmethod
	def searchForHIE(cls, **kwargs):
		if "su_id" in kwargs:
			result = cls.searchForHIEBySUID(kwargs.get("su_id"))
			if result is not None:
				return result
		if "hie_course_number" in kwargs:
			result = cls.searchForHIEByCourseNumber(kwargs.get("hie_course_number"))
			if result is not None:
				return result
		#type, name, by location, by term here
		print("searchForHIE: default endpoint reached, return NONE")
		return None

	@classmethod
	def searchForHIEBySUID(cls, su_id):
		return db.session.query(cls).filter(cls.su_id==su_id).first()

	@classmethod
	def searchForHIEByCourseNumber(cls, course_number):
		return db.session.query(cls).filter(cls.hie_course_number==course_number).first()

	# ToString method
	def __repr__(self):
		return "[HIE:id={}, SU_ID={}, Type={}, Course_Num={}, Location={}, Term={}]".format(
			self.hie_id, self.su_id, self.hie_type, self.hie_course_number, self.location_id, self.term_id)
		
	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

class Terms(db.Model):
	__tablename__ = "terms"
	term_id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.String(6))
	year = db.Column(db.Integer, nullable=False)

	def __init__(self, term, year):
		'''Constructor. Handles entry creation for the table object. All values passed are
			by this method.'''
		self.term = term.upper()
		self.year = year

	# ToString Method
	def __repr__(self):
		return "[TERM:id=%d, Term=%s, Year=%d]".format(self.term_id, self.term, self.year)
	
	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

	### Methods for the table to enable search functions for queries. Individual query per type of search. ###
	# @classmethod
	# def searchTerms(cls, term):
	# 	id = db.session.query(cls).filter(cls.term == term)
	# 	# if id is NONE:
	# 	# 	# create new term if none exists
	# 	# else:
	# 		# print(type(id))
	# 	return id

class Locations(db.Model):
	__tablename__ = "locations"
	location_id = db.Column(db.Integer, primary_key=True)
	hie_id = db.Column(db.Integer, db.ForeignKey('high_impact_expierences.hie_id'))
	city_id = db.relationship("Cities", backref="locations.city_id", lazy=True)
	country_id = db.relationship("Countries", backref="locations.country_id", lazy=True)
	london_flag = db.Column(db.Boolean)
	dc_flag = db.Column(db.Boolean)

	def __init__(self, london_flag, dc_flag):
		self.london_flag = london_flag
		self.dc_flag = dc_flag

	@classmethod
	def createLocation(cls, london_flag, dc_flag, city_name, country_name):
		print("createLocation: creating new location entry")
		newEntry = cls(london_flag, dc_flag) # call default contructor

		## Append city entry relationship ##
		city = Cities.searchForCity(loc_id=newEntry.location_id, name=city_name)
		if city is None:
			print("createLocation: city not found, creating new entry")
			city = Cities.createCity(city_name)
		else:
			print("createLocation: city found, using existing entry")
		newEntry.city_id.append(city)
		## END append city ##

		## Append country entry relationship ##
		country = Countries.searchForCountry(loc_id=newEntry.location_id, name=country_name)
		if country is None:
			print("createLocation: country not found, creating new entry")
			country = Countries.createCountry(country_name)
		else:
			print("createLocation: country found, using existing entry")
		newEntry.country_id.append(country)
		## END append country ##

		newEntry.saveToDB()
		print("createLocation: success, new entry added")
		return newEntry

	@classmethod
	def searchForLocation(cls, **kwargs):
		if "hie_id" in kwargs:
			result = cls.searchForLocationByHIEID(kwargs.get("hie_id"))
			if result is not None:
				return result
		if "city" in kwargs or "country" in kwargs:
			result = cls.searchForLocationByCityCountry(kwargs.get("city"), kwargs.get("country"))
			if result is not None:
				return result
		print("searchForLocation: default enpoint reached, returns NONE")
		return None

	@classmethod
	def searchForLocationByHIEID(cls, hie_id):
		return db.session.query(cls).filter(cls.hie_id == hie_id).first()

	@classmethod
	def searchForLocationByCityCountry(cls, city, country):
		city = db.session.query(Cities).filter(Cities.name == city).first()
		if city is None:
			country = db.session.query(Countries).filter(Countries.name == country).first()
			return country
		return None

	# ToString method
	def __repr__(self):
		return "[LOCATION:id={}, HIE_ID={}, City={}, Country={}, London?={}, DC?={}]".format(
			self.location_id, self.hie_id, self.city_id, self.country_id, self.london_flag, self.dc_flag)
		
	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

class Demographics(db.Model): 
	"""Table definition of the Demographics table. Takes/builds off of base database Model.

	__init__(self, sex, pell_flag, first_year_flag)

	createDemographic() -- creates new entry in the demographic table, will call __init__
	searchForDemographic() -- searches for entry in table based on keyword arguments
	saveToDB() -- adds and commits instance to database
	"""
	__tablename__ = "demographics"
	demographic_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	pell_flag = db.Column(db.Boolean, nullable=False)
	sex = db.Column(db.String(1), nullable=False)
	race_id = db.relationship("Races", backref='demographics.race_id', lazy=True)
	first_gen_flag = db.Column(db.Boolean, nullable=False)

	def __init__(self, sex, pell_flag, first_year_flag):
		self.pell_flag = pell_flag
		self.sex = sex
		self.first_gen_flag = first_year_flag

	@classmethod
	def createDemographic(cls, sex, pell, first_gen, first_race, second_race):
		"""Create a new entry in the Demographics table and returns the new instance. Keyword arguments
		are used to find/create a Race entry relationship.

		Parameters:
		sex (char) -- Biological sex ('M' or 'F')
		pell (bool) -- Flag indicating if entry received Pell Grant
		first_gen (bool) -- Flag indicating if entry is a first generation college student
		first_race (str) -- first race of entry (default None)
		second_race (str) -- second race of entry (default None)
		"""
		print("createDemographic: creating new entry in demographics.")
		newEntry = cls(sex, pell, first_gen) #call default constructor
		race = Races.searchForRace(first_race=first_race, second_race=second_race)
		if race is None:
			print("createDemographic: Race not found, creating new entry in Race")
			race = Races.createRace(first_race=first_race, second_race=second_race)
		else:
			print("createDemographic: race found, using existing entry")
		newEntry.race_id.append(race)
		newEntry.saveToDB()
		print("createDemographic: demographic entry added to table")
		return newEntry

	# ToString method
	def __repr__(self):
		return "[DEMOGRAPHIC:id={}, SU_ID={}, Sex={}, Race={}, Pell_Grant?={}, First_Gen?={}]".format(
			self.demographic_id, self.su_id, self.sex, self.race_id, self.pell_flag, self.first_gen_flag)

	@classmethod
	def searchForDemographic(cls, **kwargs):
		"""Search through Demographics table based on the passed column attributes.

		Keyword Arguments:
		su_id (int) -- Student ID an entry references in the Students Table
		TODO: other arguments and searches
		"""
		if "su_id" in kwargs:
			result = cls.searchForDemographicBySUID(kwargs.get("su_id"))
			if result is not None:
				return result
		# if "pell_flag" in kwargs:
		# 	result = cls.searchForDemographicByPell(kwargs.get("pell_flag"))
		# 	if result is not None:
		# 		return result
		# if "first_gen" in kwargs:
		# 	result = cls.searchForDemographicByFG(kwargs.get("first_gen"))
		# 	if result is not None:
		# 		return result
		# if "sex" in kwargs:
		# 	result = cls.searchForDemographicBySex(kwargs.get("sex"))
		# 	if result is not None:
		# 		return result
		# if "race_id" in kwargs:
		# 	result = cls.searchForDemographicByRaceID(kwargs.get("race_id"))
		# 	if result is not None:
		# 		return result
		print("searchDemographic reached default endpoint, returns NONE")
		return None

	@classmethod
	def searchForDemographicBySUID(cls, id):
		"""Returns first match by student ID"""
		return db.session.query(cls).filter(cls.su_id == id).first()

	# @classmethod
	# def searchForDemographicByPell(cls, pell):
	# 	return db.session.query(cls).filter(cls.pell_flag == pell)

	# @classmethod
	# def searchForDemographicByRaceID(cls, id):
	# 	return db.session.query(cls).filter(cls.race_id == id)

	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

class Races(db.Model):
	"""Table definition of the Races table. Takes/builds off of base database Model.

	__init__(self, first_race, second_race)

	createRace() -- creates new entry in the Race table, will call __init__
	searchForRace() -- searches for entry in table based on keyword arguments
	saveToDB() -- adds and commits instance to database
	
	"""
	__tablename__ = "races"
	race_id = db.Column(db.Integer, primary_key=True)
	demographic_id = db.Column(db.Integer, db.ForeignKey('demographics.demographic_id'))
	first_race = db.Column(db.String(20), nullable=False)
	second_race = db.Column(db.String(20))

	def __init__(self, first_race, second_race):
		self.first_race = first_race
		self.second_race = second_race

	# ToString method
	def __repr__(self):
		return "[RACE:id={}, DEMO_ID={}, Race1={}, Race2={}]".format(
			self.race_id, self.demographic_id, self.first_race, self.second_race)

	@classmethod
	def createRace(cls, first_race, second_race):
		"""Create a new entry in the Races table and returns the new instance

		Parameters:
		first_race (str) -- first race of entry (default None)
		second_race (str) -- second race of entry (default None)
		"""
		print("createRace: creating new entry in Races.")
		newEntry = cls(first_race, second_race) #call default constructor
		newEntry.saveToDB()
		print("createRace: new race added to table")
		return newEntry

	@classmethod
	def searchForRace(cls, **kwargs):
		"""Search through Races table based on the passed column attribute

		Keyword Arguments:
		demographic_id (int) -- Demographic ID an entry references in the Demographics Table
		first_race (str) -- Primary racial description
		second_race (str) -- Secondary racial description
		"""
		if "demographic_id" in kwargs:
			result = cls.searchForRaceByID(kwargs.get("demographic_id"))
			if result is not None:
				return result
		if "first_race" in kwargs:
			result = cls.searchForRaceByRace(kwargs.get("first_race"), kwargs.get("second_race"))
			return result
		print("searchRace reached default endpoint, returns NONE")
		return None

	@classmethod
	def searchForRaceByID(cls, id):
		"""Returns first match by ID"""
		return db.session.query(cls).filter(cls.demographic_id == id).first()

	@classmethod
	def searchForRaceByRace(cls, first_race, second_race):
		"""Returns first match by racial descriptions"""
		return db.session.query(cls).filter((cls.first_race == first_race) | (cls.second_race == second_race)).first()

	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

class Enrollments(db.Model):
	__tablename__ = "enrollments"
	enrollment_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	fys_aes_term = db.relationship("Terms", secondary=termToEnroll, backref='termToEnroll.term_id', lazy=True)
	fys_flag = db.Column(db.Boolean, nullable=False) # True if had FYS, False if transfered and had AES
	graduation_id = db.relationship("GraduationClasses", backref='enrollments.graduation_id', lazy=True)
	# loa_id = db.relationship("LeaveOfAbsences", backref='enrollments.loa_id', lazy=True)

	def __init__(self, su_id):
		self.su_id = su_id

	# ToString method
	def __repr__(self):
		return "[ENROLLMENT:id={}, SU_ID={}, FYS_Term={}, AES_Term={}, Grad_ID={}]".format(
			self.enrollment_id, self.su_id, self.fys_term, self.aes_term, self.graduation_id)
		
	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

class GraduationClasses(db.Model):
	__tablename__ = "graduation_class"
	graduation_id = db.Column(db.Integer, primary_key=True)
	enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.enrollment_id'))
	# su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	graduation_term = db.relationship("Terms", secondary=termToGrad, backref='termToGrad.term_id', lazy=True)
	graduated = db.Column(db.Boolean)

	def __init__(self, su_id):
		self.su_id = su_id

	# ToString method
	def __repr__(self):
		return "[GRAD_CLASS:id={}, SU_ID={}, ExpGrad={}, ActGrad={}]".format(
			self.graduation_id, self.su_id, self.expected_term, self.actual_term)
		
	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

# class LeaveOfAbsences(db.Model):
# 	__tablename__ = "leave_of_absences"
# 	loa_id = db.Column(db.Integer, primary_key=True)
# 	enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.enrollment_id'))
# 	start_term = db.relationship("Terms", secondary=termToLoa, backref='termToLoa.term_id', lazy=True)
# 	end_term = db.relationship("Terms", secondary=termToLoa, backref='termToLoa.term_id', lazy=True)
# 	loa_description = db.Column(db.Text)

# 	def __init__(self, su_id, enrollment_id, description):
# 		self.su_id = su_id
# 		self.enrollment_id = enrollment_id
# 		self.loa_description = description

# 	# ToString method
# 	def __repr__(self):
# 		return "[LOA:id=%d, SU_ID=%d, Enrollment=%d, Start=%d, End=%d \n --> Description: %s]".format(
# 			self.loa_id, self.su_id, self.enrollment_id, self.start_term, self.end_term, self.loa_description)
		
# 	def saveToDB(self):
# 		'''Quicksave method. Automatically commits and saves entry to db.'''
# 		db.session.add(self)
# 		db.session.commit()

class Cities(db.Model):
	__tablename__ = 'cities'
	city_id = db.Column(db.Integer, primary_key=True)
	loc_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
	name = db.Column(db.Text, nullable=False)

	def __init__(self, name):
		self.name = name
	
	@classmethod
	def createCity(cls, name):
		print("createCity: creating new entry")
		newEntry = cls(name)
		newEntry.saveToDB()
		print("createCity: created new entry successfully")
		return newEntry

	@classmethod
	def searchForCity(cls, **kwargs):
		if "loc_id" in kwargs:
			result = cls.searchForCityByLOCID(kwargs.get("loc_id"))
			if result is not None:
				return result
		if "name" in kwargs:
			result = cls.searchForCityByName(kwargs.get("name"))
			return result
		print("searchForCity: Default endpoint reached, returns NONE")
		return None

	@classmethod
	def searchForCityByLOCID(cls, loc_id):
		return db.session.query(cls).filter(cls.loc_id == loc_id).first()

	@classmethod
	def searchForCityByName(cls, name):
		return db.session.query(cls).filter(cls.name == name).first()

	# ToString method
	def __repr__(self):
		return "[City:id={}, Name={}, Country={}]".format(self.id, self.name, self.country_id)

	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

class Countries(db.Model):
	__tablename__ = 'countries'
	country_id = db.Column(db.Integer, primary_key=True)
	loc_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
	name = db.Column(db.Text, unique=True, nullable=False)

	def __init__(self, name):
		self.name = name
	
	@classmethod
	def createCountry(cls, name):
		print("createCountry: creating new entry")
		newEntry = cls(name)
		newEntry.saveToDB()
		print("createCountry: created new entry successfully")
		return newEntry

	@classmethod
	def searchForCountry(cls, **kwargs):
		if "loc_id" in kwargs:
			result = cls.searchForCountryByLOCID(kwargs.get("loc_id"))
			if result is not None:
				return result
		if "name" in kwargs:
			result = cls.searchForCountryByName(kwargs.get("name"))
			return result
		print("searchForCountry: Default endpoint reached, returns NONE")
		return None

	@classmethod
	def searchForCountryByLOCID(cls, loc_id):
		return db.session.query(cls).filter(cls.loc_id == loc_id).first()

	@classmethod
	def searchForCountryByName(cls, name):
		return db.session.query(cls).filter(cls.name == name).first()

	# ToString method
	def __repr__(self):
		return "[COUNTRIES:id={}, name={}]".format(self.country_id, self.name)
		
	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()

if __name__ == '__main__':
	main()
