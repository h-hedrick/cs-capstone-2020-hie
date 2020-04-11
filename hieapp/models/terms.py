from hieapp import app
from hieapp.dbcore import db
from hieapp.models.mmRelationships import *

class Terms(db.Model):
	__tablename__ = "terms"
	term_id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.String(6))
	year = db.Column(db.Integer, nullable=False)

	def __init__(self, term, year):
		'''Constructor. Handles entry creation for the table object. All values passed are
			by this method.'''
		self.term = term
		self.year = year

	@classmethod
	def createTerm(cls, term, year):
		print("createTerm: creating new term entry")
		newEntry = cls(term, year) # call default contructor
		newEntry.saveToDB()
		print("createTerm: success, new entry added")
		return newEntry

	@classmethod
	def searchForTerm(cls, term, year):
		return db.session.query(cls).filter(cls.term == term).filter(cls.year == year).first()

	# ToString Method
	def __repr__(self):
		return "[TERM:id=%d, Term=%s, Year=%d]".format(self.term_id, self.term, self.year)
	
	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()