from flask import Flask, request, jsonify, g
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from schemas import UserSchema, MedicationSchema, ProductSchema, OrderSchema, LoginSchema
from marshmallow import ValidationError
from db.alembic_orm.add import Session, User, Medication, Order, Product, RoleEnum, engine
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from contextlib import contextmanager

app = Flask(__name__)
auth = HTTPBasicAuth()
bcrypt = Bcrypt(app)
CORS(app)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    # finally:
    #     session.close()


@auth.get_user_roles
def get_user_roles(user):
    app.logger.info(user)
    return user.get_role()


@auth.verify_password
def verify_password(email, password):
    with session_scope() as session:
        user = session.query(User).filter(User.email == email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            app.logger.info(user)
            return user


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login_schema = LoginSchema()
    try:
        login_schema.load(data)
    except ValidationError as err:
        return 'invalid credentials', 400
    with session_scope() as session:
        user: User = session.query(User).filter(User.email == data['email']).first()
        if user is not None and bcrypt.check_password_hash(user.password_hash, data['password']):
            return 'login successful', 200
    return 'wrong email or password', 404


@app.route('/api/v1/hello-world-15')
def hello_world():
    return "Hello world 15"


@app.route('/users', methods=['POST'])
def create_user():
    app.logger.info('entered action')
    data = request.json
    user_schema = UserSchema()
    app.logger.info('created schema')
    parsed_data = {'email': data['email'],
                   'password_hash': bcrypt.generate_password_hash(data['password']).decode('utf-8')}
    if "role" in data:
        parsed_data['role'] = data['role']
    with session_scope() as session:
        if not session.query(User).filter(User.email == parsed_data['email']).one_or_none() is None:
            return 'email busy', 409

        try:
            user = user_schema.load(parsed_data)
        except ValidationError as err:
            return err.messages, 400
        app.logger.info('created user')
        session.add(user)
        return "created successfully", 201


@app.route('/users/current', methods=["GET"])
@auth.login_required
def get_current_user():
    with session_scope() as session:
        app.logger.info("start")
        user_schema = UserSchema(exclude=['password_hash'])
        app.logger.info(session.query(User).first())
        app.logger.info(auth.current_user())
        app.logger.info(auth.current_user().id)

        user = session.query(User).filter(User.id == auth.current_user().id).one_or_none()
        app.logger.info(user_schema.dump(user))
        return user_schema.dump(user)


@app.route('/users/current', methods=["PUT"])
@auth.login_required
def edit_current_user():
    data = request.json
    user_schema = UserSchema(exclude=['email', 'role', 'password_hash'])
    try:
        user_schema.load(data)
    except ValidationError as err:
        return err.messages, 400
    with session_scope() as session:
        found_user = session.query(User).filter(User.id == auth.current_user().id).one_or_none()
        found_user.first_name = found_user.first_name if "first_name" not in data else data["first_name"]
        found_user.last_name = found_user.last_name if "last_name" not in data else data["last_name"]
        found_user.patronymic = found_user.patronymic if "patronymic" not in data else data["patronymic"]
        found_user.phone = found_user.phone if "phone" not in data else data["phone"]
        found_user.address = found_user.address if "address" not in data else data["address"]
        return_schema = UserSchema(exclude=['password_hash'])
        return return_schema.dump(found_user), 200


@app.route('/users/current', methods=["DELETE"])
@auth.login_required
def delete_current_user():
    with session_scope() as session:
        found_user = session.query(User).filter(User.id == auth.current_user().id).one_or_none()
        session.delete(found_user)
        return ''


@app.route('/users/<user_id>')
def find_user(user_id):
    try:
        UserSchema(only=['id']).load({'id': user_id})
    except ValidationError as err:
        return 'invalid id', 400
    with session_scope() as session:
        found_user = session.query(User).filter(User.id == user_id).one_or_none()
        session.close()
        if found_user is None:
            return 'user not found', 404
        user_schema = UserSchema(exclude=['password_hash'])
        user = user_schema.dump(found_user)
        return user


@app.route('/users/<user_id>', methods=['PUT'])
@auth.login_required
def edit_user(user_id):
    data = request.json
    user_schema = UserSchema(only=["id"])
    try:
        user_schema.load({"id": user_id})
    except ValidationError as err:
        return "invalid id", 400
    user_schema = UserSchema()
    try:
        user_schema.load(data)
    except ValidationError as err:
        return "invalid data", 400
    with session_scope() as session:
        found_user = session.query(User).filter(User.id == user_id).one_or_none()
        if found_user is None:
            session.close()
            return "user not found", 404
        if auth.current_user().id != found_user.id:
            session.close()
            return "no permission", 403
        found_user.first_name = found_user.first_name if "first_name" not in data else data["first_name"]
        found_user.last_name = found_user.last_name if "last_name" not in data else data["last_name"]
        found_user.patronymic = found_user.patronymic if "patronymic" not in data else data["patronymic"]
        found_user.phone = found_user.phone if "phone" not in data else data["phone"]
        found_user.address = found_user.address if "address" not in data else data["address"]
        session.commit()
        return_schema = UserSchema(exclude=['password_hash'])
        return_user = return_schema.dump(found_user)
        return return_user


@app.route('/users/<user_id>', methods=['DELETE'])
@auth.login_required
def del_user(user_id):
    with session_scope() as session:
        found_user = session.query(User).filter(User.id == user_id).one_or_none()
        if found_user is None:
            return 'invalid id', 400
        if auth.current_user().id != found_user.id:
            return "no permission", 403
        session.delete(found_user)
        return ''


@app.route('/medications', methods=['GET'])
def get_all_meds():
    with session_scope() as session:
        medications = session.query(Medication).all()
        med_schema = MedicationSchema(many=True)
        return jsonify({"medications": med_schema.dump(medications)})


@app.route('/medications', methods=['POST'])
@auth.login_required(role=RoleEnum.provisor)
def create_med():
    with session_scope() as session:
        data = request.json
        med_schema = MedicationSchema()
        med_dict = {
            'name': data['name'],
            'description': data['description'],
            'cost': data['cost'],
            'quantity': data['quantity'],
            'on_sale': data['on_sale']
        }
        try:
            medication = med_schema.load(med_dict)
        except ValidationError as err:
            return err.messages, 400
        session.add(medication)
        return med_schema.dump(medication)


@app.route('/medications/<med_id>')
def get_med(med_id):
    validation_schema = MedicationSchema(only=['id'])
    try:
        validation_schema.load({'id': med_id})
    except ValidationError as err:
        return err.messages, 400
    with session_scope() as session:
        found_med = session.query(Medication).filter(Medication.id == med_id).one_or_none()
        app.logger.info(found_med)
        if found_med is None:
            return 'medicine not found', 404
        med_schema = MedicationSchema()
        return med_schema.dump(found_med)




@app.route('/medications/<med_id>', methods=['PUT'])
@auth.login_required(role=RoleEnum.provisor)
def change_med(med_id):
    # validate id
    try:
        MedicationSchema(only=['id']).load({'id': med_id})
    except ValidationError as err:
        return err.messages, 400
    data = request.json
    validation_schema = MedicationSchema()
    with session_scope() as session:
        found_med = session.query(Medication).filter(Medication.id == med_id).one_or_none()
        if found_med is None:
            session.close()
            return 'medicine not found', 404
        got_data = {
            'name': data['name'],
            'description': data['description'],
            'cost': data['cost'],
            'quantity': data['quantity'],
            'on_sale': data['on_sale']
        }
        try:
            validation_schema.load(got_data)
        except ValidationError as err:
            return err.messages, 400
        found_med.name = found_med.name if "name" not in data else got_data['name']
        found_med.description = found_med.description if "description" not in data else got_data['description']
        found_med.cost = found_med.cost if "cost" not in data else got_data['cost']
        found_med.quantity = found_med.quantity if "quantity" not in data else got_data['quantity']
        found_med.on_sale = found_med.on_sale if "on_sale" not in data else bool(got_data['on_sale'])
        return validation_schema.dump(found_med)


@app.route('/medications/<med_id>', methods=['DELETE'])
@auth.login_required(role=RoleEnum.provisor)
def delete_med(med_id):
    try:
        MedicationSchema(only=['id']).load({'id': med_id})
    except ValidationError as err:
        return err.messages, 400
    with session_scope() as session:
        med = session.query(Medication).filter(Medication.id == med_id).one_or_none()
        session.delete(med)
    return ''


@app.route('/store/orders', methods=['POST'])
@auth.login_required(role=RoleEnum.user)
def order_med():
    data = request.json
    app.logger.info(data)
    order_schema = OrderSchema()
    current_user_id = auth.current_user().id
    app.logger.info(current_user_id)
    app.logger.info(type(current_user_id))
    app.logger.info(type(14))
    data["user_id"] = str(auth.current_user().id)
    data["completed"] = False
    data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    app.logger.info(data["created_at"])
    app.logger.info(type(data["created_at"]))
    try:
        order = order_schema.load(data)
    except ValidationError as err:
        app.logger.info(data)
        return err.messages, 404
    with session_scope() as session:
        for product in data["products"]:
            medication = session.query(Medication).filter(Medication.id == product["med_id"]).one_or_none()
            if medication is None:
                return "medication not found", 404
            new_amount = medication.quantity - product["amount"]
            if new_amount < 0:
                return "amount is too big", 400
            medication.quantity = new_amount
        session.add(order)
        return data


@app.route('/store/orders', methods=['GET'])
@auth.login_required(role=RoleEnum.user)
def get_all_orders():
    with session_scope() as session:
        orders = session.query(Order).filter(auth.current_user().id == Order.user_id).all()
        app.logger.info(orders)
        order_schema = OrderSchema(many=True)
        return jsonify({"orders": order_schema.dump(orders)})


@app.route('/store/orders/<order_id>')
@auth.login_required
def get_order(order_id):
    try:
        OrderSchema().load({'id': order_id})
    except ValidationError as err:
        return err.messages, 400
    with session_scope() as session:
        found_order = session.query(Order).filter(Order.id == order_id).one_or_none()
        if found_order is None:
            return 'order not found', 404
        if found_order.user_id != auth.current_user().id and auth.current_user().role == RoleEnum.user:
            return 'no permission', 403
        return OrderSchema().dump(found_order)


if __name__ == "__main__":
    app.run(debug=True)
