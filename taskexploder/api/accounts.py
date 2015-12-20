from flask import g, request, jsonify
import uuid
from ..model.users import User, hash_pwd

def create_user(session, username, password):
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
        return jsonify({"status": "success", "result": account.to_dict()})

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
            "result": account.to_dict()
        })