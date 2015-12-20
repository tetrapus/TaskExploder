from ..model.tasks import Task
from flask import session, abort, g, request, jsonify

def get_subtasks(session, user, parent=None):
    return session.query(
        Task
    ).filter(
        Task.user_id == user,
        Task.parent_id == parent
    ).order_by(
        Task.idx
    ).all()

def register(blueprint):
    @blueprint.route('/tasks', methods=['GET'])
    def list_tasks():
        if not session.get('user_id'):
            abort(401)
        tasks = get_subtasks(g.db, session['user_id'], request.args.get('parent'))
        entries = [t.to_dict() for t in tasks]
        return jsonify({"status": "success", "data": entries})

    @blueprint.route('/tasks', methods=['POST'])
    def new_task():
        if not session.get('user_id'):
            abort(401)
        user_id = session['user_id']
        try:
            title = request.form['title']
            if len(title) > 140:
                return jsonify({"status": "error", "error": "Title must be under 140 characters."})
        except KeyError:
            return jsonify({"status": "error", "error": "Must supply title."})
        parent_id = request.form.get('parent_id') # TODO: Validate me
        points = request.form.get('points')
        status = request.form.get('status')
        idx = request.form.get('idx')
        try:
            task = Task(
                user_id=user_id,
                title=title,
                parent_id=parent_id,
                points=points,
                status=status,
                idx=idx
            )
            g.db.add(task)
            g.db.commit()
        except:
            return jsonify({"status": "error", "error": "Task creation failed."})
        return jsonify({"status": "success", "result": task.to_dict()})

    @blueprint.route('/tasks/<task_id>', methods=['POST'])
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
            return jsonify({"status": "error", "error": "Title must be under 140 characters."})
        # TODO: Validate parent

        results = g.db.query(
            Task
        ).filter(
            Task.user_id == user_id,
            Task.id == task_id
        ).update(
            updates
        )
        g.db.commit()
        if results:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"})

    # def delete_entry():
    #     pass

