from hieapp import app
from hieapp.dbcore import db    
from hieapp.models.cities import *
from hieapp.models.countries import *

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
