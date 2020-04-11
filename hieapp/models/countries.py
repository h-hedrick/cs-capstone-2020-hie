from hieapp import app
from hieapp.dbcore import db

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
