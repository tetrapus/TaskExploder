from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


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

class TaskStatus(object):
    ACTIVE = 0
    DONE = 1
    DELETED = 2

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('tasks.id'))
    title = Column(String)
    points = Column(Integer)
    status = Column(Integer)
    idx = Column(Integer)

    def to_dict(self):
        return {
            "type": "Task",
            "id": self.id,
            "user_id": self.user_id,
            "parent_id": self.parent_id,
            "title": self.title,
            "points": self.points,
            "status": self.status,
            "idx": self.idx
        }