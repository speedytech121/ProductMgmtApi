from marshmallow import Schema, fields, validate
class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str()
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
