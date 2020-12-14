from marshmallow import Schema, fields, post_load
from db.alembic_orm.add import User, Medication, Order, Demand

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    username = fields.Str()
    password_hash = fields.Str()

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)

class MedicationSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    cost = fields.Int()
    quantity = fields.Int()
    in_stock = fields.Bool()

    @post_load
    def create_medication(self, data, **kwargs):
        return Medication(**data)

class OrderSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    med_id = fields.Int()
    amount = fields.Int()
    completed = fields.Bool()

    @post_load
    def create_order(self, data, **kwargs):
        return Order(**data)

class DemandSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    med_id = fields.Int()
    amount = fields.Int()

    @post_load
    def create_demand(self, data, **kwargs):
        return Demand(**data)
