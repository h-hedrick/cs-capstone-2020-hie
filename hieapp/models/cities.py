from hieapp import app
from hieapp.dbcore import db

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
