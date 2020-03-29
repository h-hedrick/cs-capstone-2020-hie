from hieapp.dbcore import db

termToHIE = db.Table('term_hie',
	db.Column('term_id', db.Integer, db.ForeignKey('terms.term_id')),
	db.Column('hie_id', db.Integer, db.ForeignKey('high_impact_expierences.hie_id'))
)

termToGrad = db.Table('term_grad',
	db.Column('term_id', db.Integer, db.ForeignKey('terms.term_id')),
	db.Column('grad_id', db.Integer, db.ForeignKey('graduation_class.graduation_id'))
)

termToEnroll = db.Table('term_enroll',
	db.Column('term_id', db.Integer, db.ForeignKey('terms.term_id')),
	db.Column('enrollment_id', db.Integer, db.ForeignKey('enrollments.enrollment_id'))
)