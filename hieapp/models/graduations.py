from hieapp import app
from hieapp.dbcore import db
from  hieapp.models.terms import *
from hieapp.models.mmRelationships import termToGrad

class GraduationClasses(db.Model):
	__tablename__ = "graduation_class"
	graduation_id = db.Column(db.Integer, primary_key=True)
	enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.enrollment_id'))
	# su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	graduation_term = db.relationship("Terms", secondary=termToGrad, backref='termToGrad.term_id', lazy=True)
	graduated = db.Column(db.Boolean)

	def __init__(self, graduated):
		self.graduated = graduated

	@classmethod
	def createGraduation(cls, graduated, term, year):
		print("createGraduation: start")
		newEntry = cls(graduated)
		termEntry = Terms.searchForTerm(term, year)
		if termEntry is None:
			print("createGraduation: no matching term entry found, creating new entry")
			termEntry = Terms.createTerm(term, year)
		else:
			print("createGraducation: Term found, using existing entry")
		newEntry.graduation_term.append(termEntry)
		newEntry.saveToDB()
		print("createGraduation: success")
		return newEntry

	@classmethod
	def searchForGraduation(cls, **kwargs):
		if "enrollment_id" in kwargs:
			result = cls.searchForGraduationByEnrollmentID(kwargs.get("enrollment_id"))
			if result is not None:
				return result
		#TODO:other searches here
		print("searchForGraduation failed, return NONE")
		return None

	@classmethod
	def searchForGraduationByEnrollmentID(cls, enrollment_id):
		return db.session.query(cls).filter(cls.enrollment_id == enrollment_id).first()

	# ToString method
	def __repr__(self):
		return "[GRAD_CLASS:id={}, SU_ID={}, ExpGrad={}, ActGrad={}]".format(
			self.graduation_id, self.su_id, self.expected_term, self.actual_term)
		
	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()
