''' API methods related to user accounts '''
import uuid

from flask import g, request, jsonify, session, abort

from ..model.users import User, hash_pwd


def create_user(database, username, password):
    ''' Insert a user into the database '''
    # TODO: Check username is unique
    # Generate a salt
    salt = uuid.uuid4().hex
    password_hash = hash_pwd(password, salt)

    user = User(
        username=username,
        password=password_hash,
        salt=salt
    )
    database.add(user)
    database.commit()

    return user


def create_account():
    ''' Register a new user '''
    account = create_user(g.db, request.form['username'], request.form['password'])
    return jsonify({"status": "success", "data": account.to_dict()})


def get_account():
    ''' Get a user object by username '''
    account = User.from_username(g.db, request.args['username'])
    if account is None:
        return jsonify({
            'status': 'error',
            'message': 'User does not exist.'
        })
    return jsonify({
        "status": "success",
        "data": account.to_dict()
    })


def get_current_user():
    ''' Return the user object associate with the current session '''
    if not session.get('user'):
        abort(401)
    return jsonify({
        'status': 'success',
        'data': session.get('user'),
    })


def register(blueprint):
    ''' Register account endpoints '''
    blueprint.route('/account', methods=['POST'])(create_account)

    blueprint.route('/account', methods=['GET'])(get_account)

    blueprint.route("/whoami", methods=["GET"])(get_current_user)
