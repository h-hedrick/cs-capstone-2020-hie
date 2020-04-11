from hieapp import app
from hieapp.dbcore import db
from hieapp.models.races import *

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
