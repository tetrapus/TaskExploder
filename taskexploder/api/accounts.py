import uuid

from flask import g, request, jsonify, session, abort

from ..model.users import User, hash_pwd


def create_user(session, username, password):
    # TODO: Check username is unique
    # Generate a salt
    salt = uuid.uuid4().hex
    password_hash = hash_pwd(password, salt)

    user = User(
        username=username,
        password=password_hash,
        salt=salt
    )
    session.add(user)
    session.commit()

    return user


def register(blueprint):
    @blueprint.route('/account', methods=['POST'])
    def create_account():
        account = create_user(g.db, request.form['username'], request.form['password'])
        return jsonify({"status": "success", "data": account.to_dict()})

    @blueprint.route('/account', methods=['GET'])
    def get_account():
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

    @blueprint.route("/whoami", methods=["GET"])
    def get_current_user():
        if not session.get('user'):
            abort(401)
        return jsonify({
            'status': 'success',
            'data': session.get('user'),
        })
