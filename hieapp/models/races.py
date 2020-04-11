from hieapp import app
from hieapp.dbcore import db

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
