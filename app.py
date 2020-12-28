from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from schemas import UserSchema, MedicationSchema, DemandSchema, OrderSchema
from marshmallow import ValidationError
from db.alembic_orm.add import Session, User, Medication, Order, Demand, RoleEnum
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
bcrypt = Bcrypt(app)
session = Session()


@auth.get_user_roles
def get_user_roles(user):
    return user.get_role()


@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter(User.username == username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return user


@app.route('/api/v1/hello-world-15')
def hello_world():
    return "Hello world 15"


@app.route('/users', methods=['POST'])
def create_user():
    app.logger.info('entered action')
    data = request.json
    user_schema = UserSchema()
    app.logger.info('created schema')
    parsed_data = {'username': data['username'], 'email': data['email'],
                   'password_hash': bcrypt.generate_password_hash(data['password']).decode('utf-8')}
    if "role" in data:
        parsed_data['role'] = data['role']
    if not session.query(User).filter(User.username == parsed_data['username']).one_or_none() is None:
        return 'username busy', 400

    try:
        user = user_schema.load(parsed_data)
    except ValidationError as err:
        return err.messages, 400
    app.logger.info('created user')
    session.add(user)
    session.commit()
    return user_schema.dump(user), 201


@app.route('/users/<user_id>')
def find_user(user_id):
    try:
        UserSchema(only=['id']).load({'id': user_id})
    except ValidationError as err:
        return 'invalid id', 400
    found_user = session.query(User).filter(User.id == user_id).one_or_none()
    if found_user is None:
        return 'user not found', 404
    user_schema = UserSchema(exclude=['password_hash'])
    user = user_schema.dump(found_user)
    return user


def validate_update(data, user_id):
    # got_id = data['id']
    found_user = session.query(User).filter(User.id == user_id).one_or_none()
    if found_user is None:
        raise ValidationError(message='invalid id')
    username = data['username']
    username_user = session.query(User).filter(User.username == username).one_or_none()
    if found_user.username != username and not username_user is None:
        raise ValidationError(message='username is busy')
    user_data = {'username': data['username'], 'email': data['email']}
    schema = UserSchema()
    schema.load(user_data)


@app.route('/users/<user_id>', methods=['PUT'])
@auth.login_required
def edit_user(user_id):
    data = request.json
    try:
        validate_update(data, user_id)
    except ValidationError as err:
        return jsonify(err.messages), 400
    found_user = session.query(User).filter(User.id == user_id).one_or_none()
    if auth.current_user().id != found_user.id:
        return "no permission", 403
    found_user.username = data['username']
    found_user.email = data['email']
    # found_user.role = data['role']
    session.commit()
    return_schema = UserSchema(exclude=['password_hash'])
    return_user = return_schema.dump(found_user)
    return return_user


@app.route('/users/<user_id>', methods=['DELETE'])
@auth.login_required
def del_user(user_id):
    found_user = session.query(User).filter(User.id == user_id).one_or_none()
    if found_user is None:
        return 'invalid id', 400
    if auth.current_user().id != found_user.id:
        return "no permission", 403
    session.delete(found_user)
    session.commit()
    return ''


@app.route('/medications', methods=['POST'])
@auth.login_required(role=RoleEnum.provisor)
def create_med():
    data = request.json
    med_schema = MedicationSchema()
    med_dict = {'name': data['name'], 'description': data['description'], 'cost': data['cost'], 'quantity': data['quantity'], 'in_stock': data['inStock']}
    try:
        medication = med_schema.load(med_dict)
    except ValidationError as err:
        return err.messages, 400
    session.add(medication)
    session.commit()
    return med_schema.dump(medication)


@app.route('/medications/<med_id>')
def get_med(med_id):
    validation_schema = MedicationSchema(only=['id'])
    try:
        validation_schema.load({'id': med_id})
    except ValidationError as err:
        return err.messages, 400
    found_med = session.query(Medication).filter(Medication.id == med_id).one_or_none()
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
    found_med = session.query(Medication).filter(Medication.id == med_id).one_or_none()
    if found_med is None:
        return 'medicine not found', 404
    got_data = {
        'name': data['name'],
        'description': data['description'],
        'cost': data['cost'],
        'quantity': data['quantity'],
        'in_stock': data['inStock']
    }
    try:
        validation_schema.load(got_data)
    except ValidationError as err:
        return err.messages, 400
    found_med.name = got_data['name']
    found_med.description = got_data['description']
    found_med.cost = got_data['cost']
    found_med.quantity = got_data['quantity']
    found_med.in_stock = bool(got_data['in_stock'])
    session.commit()
    return validation_schema.dump(found_med)


@app.route('/medications/<med_id>', methods=['DELETE'])
@auth.login_required(role=RoleEnum.provisor)
def delete_med(med_id):
    try:
        MedicationSchema(only=['id']).load({'id': med_id})
    except ValidationError as err:
        return err.messages, 400
    med = session.query(Medication).filter(Medication.id == med_id).one_or_none()
    session.delete(med)
    session.commit()
    return ''


@app.route('/store/orders', methods=['POST'])
@auth.login_required(role=RoleEnum.user)
def order_med():
    data = request.json
    # cretatng schema just for validation
    validation_schema = OrderSchema()
    got_data = {
        #'user_id': data['userId'],
        'user_id': auth.current_user().id,
        'med_id': data['medicationId'],
        'amount': data['amount']
    }
    # executing validation by field type
    try:
        validation_schema.load(got_data)
    except ValidationError as err:
        return err.messages, 400
    # checking the medicine
    found_med = session.query(Medication).filter(Medication.id == got_data['med_id']).one_or_none()
    if found_med is None:
        return 'medicine not found', 400
    # business logic
    if found_med.quantity < int(got_data['amount']):
        demand_schema = DemandSchema()
        demand = demand_schema.load(got_data)
        session.add(demand)
        session.commit()
        return demand_schema.dump(got_data), 201
    else:
        got_data['completed'] = 'false'
        found_med.quantity -= int(got_data['amount'])
        if found_med.quantity == 0:
            found_med.in_stock = False
        order = validation_schema.load(got_data)
        session.add(order)
        session.commit()
        return validation_schema.dump(got_data)


@app.route('/store/orders/<order_id>')
@auth.login_required
def get_order(order_id):
    try:
        OrderSchema().load({'id': order_id})
    except ValidationError as err:
        return err.messages, 400
    found_order = session.query(Order).filter(Order.id == order_id).one_or_none()
    if found_order is None:
        return 'order not found', 404
    if found_order.user_id != auth.current_user().id and auth.current_user().role == RoleEnum.user:
        return 'no permission', 403
    return OrderSchema().dump(found_order)


@app.route('/store/demands')
@auth.login_required(role=RoleEnum.provisor)
def get_demands():
    found_demands = session.query(Demand).all()
    return jsonify(DemandSchema(many=True).dump(found_demands))


if __name__ == "__main__":
    app.run(debug=True)
