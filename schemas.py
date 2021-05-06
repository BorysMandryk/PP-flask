from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from db.alembic_orm.add import User, Medication, Order, Product, RoleEnum


class MedicationSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str()
    cost = fields.Int()
    quantity = fields.Int()
    on_sale = fields.Bool(required=True)

    @post_load
    def create_medication(self, data, **kwargs):
        return Medication(**data)


class ProductSchema(Schema):
    id = fields.Int()
    amount = fields.Int(required=True)
    med_id = fields.Int(required=True)
    order_id = fields.Int()

    @post_load
    def create_product(self, data, **kwargs):
        return Product(**data)


class OrderSchema(Schema):
    id = fields.Int()
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    completed = fields.Bool(required=True)
    products = fields.Nested(ProductSchema, many=True, required=True)

    @post_load
    def create_order(self, data, **kwargs):
        return Order(**data)


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email(required=True)
    first_name = fields.Str()
    last_name = fields.Str()
    patronymic = fields.Str()
    password_hash = fields.Str(required=True)
    phone = fields.Str()
    address = fields.Str()
    orders = fields.Nested(OrderSchema, many=True)
    role = EnumField(RoleEnum, default=RoleEnum.user, missing="user")

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
