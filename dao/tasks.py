from .types import Task

def get_subtasks(session, user, parent=None):
    return session.query(
        Task
    ).filter(
        Task.user_id == user,
        Task.parent_id == parent
    ).order_by(
        Task.idx
    ).all()
