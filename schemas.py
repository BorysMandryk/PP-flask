from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from db.alembic_orm.add import User, Medication, Order, Demand, RoleEnum


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
    medications = fields.Nested(MedicationSchema)

    @post_load
    def create_order(self, data, **kwargs):
        return Order(**data)


class DemandSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    med_id = fields.Int()
    amount = fields.Int()
    medications = fields.Nested(MedicationSchema)

    @post_load
    def create_demand(self, data, **kwargs):
        return Demand(**data)


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    username = fields.Str()
    password_hash = fields.Str()
    orders = fields.List(fields.Nested(OrderSchema))
    demands = fields.List(fields.Nested(DemandSchema))
    role = EnumField(RoleEnum, default=RoleEnum.user, missing="user")

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
