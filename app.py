from flask import Flask, request, abort
from flask_bcrypt import Bcrypt
from schemas import UserSchema, MedicationSchema, DemandSchema, OrderSchema
from marshmallow import ValidationError
from db.alembic_orm.add import Session, User

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
        return abort(400, 'username busy')

    try:
        user = user_schema.load(parsed_data)
    except ValidationError as err:
        return abort(400, err.messages)
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
        return abort(400, 'invalid username')

    password_ok = bcrypt.check_password_hash(found_user.password_hash, password)
    if not password_ok:
        return abort(400, 'invalid password')
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
        return abort(400, 'invalid id')
    if found_user is None:
        return abort(404, 'user not found')
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
        return abort(400, err.messages)
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
        return abort(400, 'invalid id')
    session.delete(found_user)
    session.commit()
    return ''


if __name__ == "__main__":
    app.run()
