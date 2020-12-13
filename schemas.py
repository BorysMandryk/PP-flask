from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    username = fields.Str()
    password = fields.Str()

class MedicationSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    cost = fields.Int()
    quantity = fields.Int()
    in_stock = fields.Bool()

class OrderSchema(Schema):
    id = fields.Int()
    user = fields.Nested(UserSchema)
    medication = fields.Nested(MedicationSchema)
    amount = fields.Int()
    completed = fields.Bool()

class DemandSchema(Schema):
    id = fields.Int()
    user = fields.Nested(UserSchema)
    medication = fields.Nested(MedicationSchema)
    amount = fields.Int()
