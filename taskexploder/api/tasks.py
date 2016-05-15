from datetime import datetime

from flask import session, abort, g, request, jsonify

from ..model.tasks import Task
from ..common import invalid_request


def get_subtasks(database, user, parent=None):
    """ Query for tasks from a user with a given parent """
    return database.query(Task).filter(
        Task.user_id == user,
        Task.parent_id == parent
    ).order_by(Task.idx).all()


def get_task_by_id(database, user, task):
    ''' Query for a task owned by user '''
    return database.query(Task).filter(
        Task.user_id == user,
        Task.id == task
    ).one_or_none()


def list_tasks():
    """ Return a list of tasks with a given parent """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to list your tasks."
        }), 401
    tasks = get_subtasks(g.db, user_id, request.args.get('parent'))
    entries = [t.to_dict() for t in tasks]
    return jsonify({"status": "success", "data": entries})


def new_task():
    """ Create a new task """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to create a task."
        }), 401

    try:
        title = request.form['title']
        if len(title) > 140:
            return invalid_request("Title must be under 140 characters.")
    except KeyError:
        return invalid_request("No task title provided.")

    parent_id = request.form.get('parent_id')
    if parent_id is not None:
        parent = get_task_by_id(g.db, user_id, parent_id)
        if parent is None:
            return invalid_request("Parent task could not be found.")

    points = request.form.get('points')
    if points is not None:
        try:
            points = int(points)
        except ValueError:
            return invalid_request("Points must be a valid integer.")
        else:
            if not 0 <= points < 1000:
                return invalid_request("Points must be an integer between 0 and 999.")

    status = request.form.get('status')
    try:
        status = int(status)
        if not 0 <= status < 5:
            return invalid_request("Status code not found.")
    except ValueError:
        return invalid_request("Status must be an integer between 0 and 4")
    idx = request.form.get('idx')
    try:
        idx = int(idx) if idx is not None else 0
    except ValueError:
        return invalid_request("Index must be a valid integer.")
    try:
        task = Task(
            user_id=user_id,
            title=title,
            parent_id=parent_id,
            points=points,
            status=status,
            idx=idx,
            created=datetime.now(),
        )
        g.db.add(task)
        g.db.commit()
    except:
        return jsonify({"status": "error", "message": "Task creation failed."})
    return jsonify({"status": "success", "result": task.to_dict()})


def update_entry(task_id):
    user_id = session.get('user_id')
    if not user_id:
        abort(401)

    fields = {
        Task.title: 'title',
        Task.parent_id: 'parent_id',
        Task.points: 'points',
        Task.status: 'status',
        Task.idx: 'idx'
    }

    updates = {k: request.form[v] for k, v in fields.items() if v in request.form}

    if 'title' in updates and len(updates['title']) > 140:
        return jsonify({"status": "error", "message": "Title must be under 140 characters."})
    # TODO: Validate parent

    results = g.db.query(Task).filter(
        Task.user_id == user_id,
        Task.id == task_id
    ).update(updates)
    g.db.commit()

    if results:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"})


def delete_entry():
    pass


def register(blueprint):
    blueprint.route('/tasks', methods=['GET'])(list_tasks)

    blueprint.route('/tasks', methods=['POST'])(new_task)

    blueprint.route('/tasks/<task_id>', methods=['POST'])(update_entry)
