import uuid
import hashlib
from .types import User

def hash_pwd(password, salt):
    return hashlib.sha224((password + salt).encode('utf-8')).hexdigest()

def authenticate(user, password):
    return hash_pwd(password, user.salt) == user.password

def from_username(session, username):
    return session.query(User).filter(User.username == username).one_or_none()

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
