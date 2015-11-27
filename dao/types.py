from calendar import timegm

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list

Base = declarative_base()

def epoch_of(timestamp):
    if timestamp is not None:
        return timegm(timestamp.timetuple())


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
    PENDING = 3
    EXPIRED = 4 # Expired is a variant of active, with the same semantics.

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('tasks.id'))
    title = Column(String)
    points = Column(Integer)
    status = Column(Integer)
    idx = Column(Integer)
    description = Column(String)

    created = Column(DateTime)
    activates = Column(DateTime)
    expires = Column(DateTime)

    subtasks = relationship("Task", order_by="Task.idx", collection_class=ordering_list('idx'))

    def to_dict(self):
        return {
            "type": "Task",
            "id": self.id,
            "user_id": self.user_id,
            "parent_id": self.parent_id,
            "title": self.title,
            "points": self.points,
            "status": self.status,
            "idx": self.idx,
            "description": self.description,
            "subtasks": [i.to_dict() for i in self.subtasks],
            "created": epoch_of(self.created),
            "activates": epoch_of(self.created),
            "expires": epoch_of(self.created)
        }