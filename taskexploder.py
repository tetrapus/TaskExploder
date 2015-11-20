import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
import dao.accounts
import dao.tasks
from dao.types import Task, User

app = Flask(__name__)
app.config.from_envvar('TASKEXPLODER_CONFIG', silent=True)

def make_db_session():
    return sessionmaker(bind=create_engine('sqlite:///' + app.config['DATABASE'], echo=True))()

@app.before_request
def before_request():
    g.db = make_db_session()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    if not session.get('user_id'):
        abort(401)
    tasks = dao.tasks.get_subtasks(g.db, session['user_id'], request.args.get('parent'))
    entries = [t.to_dict() for t in tasks]
    return jsonify({"status": "success", "data": entries})

@app.route('/api/tasks', methods=['POST'])
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

@app.route('/api/tasks/<task_id>', methods=['POST'])
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

@app.route('/api/account', methods=['POST'])
def create_account():
    account = dao.accounts.create_user(g.db, request.form['username'], request.form['password'])
    return jsonify({"status": "success", "result": account.to_dict()})

@app.route('/api/account', methods=['GET'])
def get_account():
    account = dao.accounts.from_username(g.db, request.args['username'])
    if account is None:
        return jsonify({
            'status': 'error',
            'message': 'User does not exist.'
        })
    return jsonify({
        "status": "success", 
        "result": account.to_dict()
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        account = dao.accounts.from_username(g.db, request.form['username'])
        if account is not None and dao.accounts.authenticate(account, request.form['password']):
            session['user_id'] = account.id
            session['user'] = account.to_dict()
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/')
def index():
    account = session.get('user')
    return render_template('index.html', account=account)

if __name__ == '__main__':
    app.run()