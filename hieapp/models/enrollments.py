from hieapp import app
from hieapp.dbcore import db
from hieapp.models.graduations import *
from hieapp.models.terms import *
from hieapp.models.mmRelationships import termToEnroll

class Enrollments(db.Model):
	__tablename__ = "enrollments"
	enrollment_id = db.Column(db.Integer, primary_key=True)
	su_id = db.Column(db.Integer, db.ForeignKey('students.su_id'))
	fys_aes_term = db.relationship("Terms", secondary=termToEnroll, backref='termToEnroll.term_id', lazy=True)
	fys_flag = db.Column(db.Boolean, nullable=False) # True if had FYS, False if transfered and had AES
	graduation_id = db.relationship("GraduationClasses", backref='enrollments.graduation_id', lazy=True)
	# loa_id = db.relationship("LeaveOfAbsences", backref='enrollments.loa_id', lazy=True)

	def __init__(self, fys_flag):
		self.fys_flag = fys_flag

	@classmethod
	def createEnrollment(cls, fys_flag, fys_aes_term, fys_aes_year, graduated, grad_term, grad_year):
		print("createEnrollment: start")
		newEntry = cls(fys_flag)

		## Append FYS/AES Term relationship ##
		fysTermEntry = Terms.searchForTerm(fys_aes_term, fys_aes_year)
		if fysTermEntry is None:
			print("createEnrollment: no matching term entry found, creating new entry")
			fysTermEntry = Terms.createTerm(fys_aes_term, fys_aes_year)
		else:
			print("createEnrollment: Term found, using existing entry")
		newEntry.fys_aes_term.append(fysTermEntry)
		## END FYS/AES Relationship ##

		## Append Graduation relationship ##
		gradEntry = GraduationClasses.searchForGraduation(enrollment_id=newEntry.enrollment_id)
		if gradEntry is None:
			print("createEnrollment: no graduation class found, creating new entry")
			gradEntry = GraduationClasses.createGraduation(graduated, grad_term, grad_year)
		else:
			print("createEnrollment: graduation found, using existing entry")
		newEntry.graduation_id.append(gradEntry)
		newEntry.saveToDB()
		print("createEnrollment: success")
		return newEntry

	@classmethod
	def searchForEnrollment(cls, **kwargs):
		if "su_id" in kwargs:
			return cls.searchForEnrollmentBySUID(kwargs.get("su_id"))
		#TODO: add other searches
		print("search default reached, returns NONE")
		return None

	@classmethod
	def searchForEnrollmentBySUID(cls, id):
		return db.session.query(cls).filter(cls.su_id == id).first()

	# ToString method
	def __repr__(self):
		return "[ENROLLMENT:id={}, SU_ID={}, FYS_Term={}, AES_Term={}, Grad_ID={}]".format(
			self.enrollment_id, self.su_id, self.fys_term, self.aes_term, self.graduation_id)
		
	def saveToDB(self):
		'''Quicksave method. Automatically commits and saves entry to db.'''
		db.session.add(self)
		db.session.commit()
