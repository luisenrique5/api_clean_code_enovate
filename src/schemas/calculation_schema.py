from marshmallow import Schema, fields, validate

class WellSchema(Schema):
    well_id = fields.String(required=True)
    separator_type = fields.String(required=True)
    fcat = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    water_cut = fields.Float(required=True, validate=validate.Range(min=0, max=100))
