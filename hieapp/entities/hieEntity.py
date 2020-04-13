#JSON entity schema for HIE data pass

from marshmallow import Schema, fields

class hieSchema(Schema):
	hie_id = fields.Number()
	hie_type = fields.String()
	hie_name = fields.String()
	hie_courseNumber = fields.String()
	hie_term = fields.String()
	hie_location = fields.String()