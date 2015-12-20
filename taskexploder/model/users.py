import hashlib

from sqlalchemy import Column, Integer, String

from . import Base


def hash_pwd(password, salt):
    return hashlib.sha224((password + salt).encode('utf-8')).hexdigest()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    salt = Column(String)

    def to_dict(self):
        return {
            "type": "User",
            "id": self.id, 
            "username": self.username
        }

    def authenticate(self, password):
        return hash_pwd(password, self.salt) == self.password

    @classmethod
    def from_username(cls, session, username):
        return session.query(cls).filter(cls.username == username).one_or_none()