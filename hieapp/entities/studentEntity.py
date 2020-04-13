#JSON entity schema for student data pass

from marshmallow import Schema, fields

class studentSchema(Schema):
	su_id = fields.Number()
	hies = fields.List()
	# TODO: should this convert to a year designation instead? add grad year seperate?
	enrollment_id = fields.Number()
	demographic_id = fields.Number()

