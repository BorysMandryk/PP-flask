from flask import Flask, request
from flask_bcrypt import Bcrypt
from schemas import UserSchema, MedicationSchema, DemandSchema, OrderSchema
from marshmallow import ValidationError
from db.alembic_orm.add import Session, User, Medication, Order, Demand

app = Flask(__name__)
bcrypt = Bcrypt(app)
session = Session()


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
    if not session.query(User).filter(User.username == parsed_data['username']).one_or_none() is None:
        return 'username busy', 400

    try:
        user = user_schema.load(parsed_data)
    except ValidationError as err:
        return err.messages, 400
    app.logger.info('created user')
    session.add(user)
    session.commit()
    # TODO return token
    return 'token placeholder'


@app.route('/users/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    found_user = session.query(User).filter(User.username == username).one_or_none()
    if found_user is None:
        return 'invalid username', 400

    password_ok = bcrypt.check_password_hash(found_user.password_hash, password)
    if not password_ok:
        return 'invalid password', 400
    # TODO replace with token generation
    return 'token placeholder'


@app.route('/users/logout')
def logout():
    # TODO discard the token
    return 'logged out'


@app.route('/users/<user_id>')
def find_user(user_id):
    found_user = session.query(User).filter(User.id == user_id).one_or_none()
    schema = UserSchema()
    try:
        schema.dump(found_user)
    except ValidationError as err:
        return 'invalid id', 400
    if found_user is None:
        return 'user not found', 404
    user_schema = UserSchema(exclude=['password_hash'])
    user = user_schema.dump(found_user)
    return user


def validate_update(data):
    got_id = data['id']
    found_user = session.query(User).filter(User.id == got_id).one_or_none()
    if found_user is None:
        raise ValidationError(message='invalid id')
    username = data['username']
    username_user = session.query(User).filter(User.username == username).one_or_none()
    if found_user is username_user:
        raise ValidationError(message='username is busy')
    user_data = {'username': data['username'], 'email': data['email']}
    schema = UserSchema()
    schema.dump(user_data)


@app.route('/users', methods=['PUT'])
def edit_user():
    data = request.json
    try:
        validate_update(data)
    except ValidationError as err:
        return err.messages, 400
    found_user = session.query(User).filter(User.id == data['id']).one_or_none()
    found_user.username = data['username']
    found_user.email = data['email']
    session.commit()
    return_schema = UserSchema(exclude=['password_hash'])
    return_user = return_schema.dump(found_user)
    return return_user


@app.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    found_user = session.query(User).filter(User.id == user_id).one_or_none()
    if found_user is None:
        return 'invalid id', 400
    session.delete(found_user)
    session.commit()
    return ''


@app.route('/medications', methods=['POST'])
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


@app.route('/medications', methods=['PUT'])
def change_med():
    data = request.json
    validation_schema = MedicationSchema()
    found_med = session.query(Medication).filter(Medication.id == data['id']).one_or_none()
    if found_med is None:
        return 'medicine not found', 404
    got_data = {
        'id': data['id'],
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
    found_med.in_stock = got_data['in_stock']
    session.commit()
    return validation_schema.dump(found_med)


if __name__ == "__main__":
    app.run()
