from hieapp.dbcore import db
from hieapp import app
from hieapp.models.locations import *
from hieapp.models.terms import *
from hieapp.models.mmRelationships import termToHIE

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
	def createHIE(cls, hie_type, hie_name, hie_course_number, london_flag, dc_flag, city_name, country_name, hie_term, hie_year):
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
		termEntry = Terms.searchForTerm(term=hie_term, year=hie_year)
		if termEntry is None:
			print("createHIE: term not found, creating new entry")
			termEntry = Terms.createTerm(hie_term, hie_year)
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