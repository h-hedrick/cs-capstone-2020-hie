# """
# 	Initialization file for the database.
# 	Script will define the logical model of the mysql database.
# 	Then will call other scripts to populate the database with the data
# 	specifically related to a csv file.
# """
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# # Set working directory
# setwd = "./sql_scripts/csv_files/"
# app = Flask(__name__)
# yam = yaml.load(open('db.yaml'))
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #suppress warnings
# # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{}:{}@{}/{}".format(
# # # 			yam["mysql_user"],
# # # 			yam["mysql_password"],
# # # 			yam["mysql_host"],
# # # 			yam["mysql_db"])
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/Users/Matt/Documents/GitHub/cs-capstone-2020-hie/sql_scripts/testdb.db"
# db = SQLAlchemy(app)

# def main():
# 	# print("Building database: {}".format(yam['mysql_db']))
# 	init_model()
# 	print("Database Built, surprisingly")
# 	# CSV Calls
# 	# print("Database Populated")

# def init_model():
# 	"""Initializes the database and database tables with relationships"""
# 	'''
# 	create database
# 		if the database doesnt exist, does the URI fail?
# 		can I use this init to create the database?
# 	call method to create each table + relations
# 	commit

# 	'''
# 	db.drop_all()
# 	db.create_all()
# 	db.session.commit()

# 	Students.createStudent(9876, "M", False, False, "White", None, "SCOPE", "DGLOS", "-1", False, False, "Georgetown", "USA", "Summer", 2017, True, "fall", 2016, False, "spring", 2020)

# ###########################################
# # Database Table Model and Relationships  #
# ###########################################

# # models moved to individual files under models folder

# # termToLoa = db.Table('term_loa',
# # 	db.Column('term_id', db.Integer, db.ForeignKey('terms.term_id')),
# # 	db.Column('loa_id', db.Integer, db.ForeignKey('leave_of_absences.loa_id'))
# # )

# # class LeaveOfAbsences(db.Model):
# # 	__tablename__ = "leave_of_absences"
# # 	loa_id = db.Column(db.Integer, primary_key=True)
# # 	enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.enrollment_id'))
# # 	start_term = db.relationship("Terms", secondary=termToLoa, backref='termToLoa.term_id', lazy=True)
# # 	end_term = db.relationship("Terms", secondary=termToLoa, backref='termToLoa.term_id', lazy=True)
# # 	loa_description = db.Column(db.Text)

# # 	def __init__(self, su_id, enrollment_id, description):
# # 		self.su_id = su_id
# # 		self.enrollment_id = enrollment_id
# # 		self.loa_description = description

# # 	# ToString method
# # 	def __repr__(self):
# # 		return "[LOA:id=%d, SU_ID=%d, Enrollment=%d, Start=%d, End=%d \n --> Description: %s]".format(
# # 			self.loa_id, self.su_id, self.enrollment_id, self.start_term, self.end_term, self.loa_description)
		
# # 	def saveToDB(self):
# # 		'''Quicksave method. Automatically commits and saves entry to db.'''
# # 		db.session.add(self)
# # 		db.session.commit()

# if __name__ == '__main__':
# 	main()
