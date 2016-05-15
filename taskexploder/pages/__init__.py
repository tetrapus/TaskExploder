from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g

from ..model.users import User


blueprint = Blueprint("Pages", __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        account = User.from_username(g.db, request.form['username'])
        if account is not None and account.authenticate(request.form['password']):
            session['user_id'] = account.id
            session['user'] = account.to_dict()
            flash('You were logged in')
            return redirect(url_for('Pages.index'))
    return render_template('login.html', error=error)


@blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('Pages.login'))


@blueprint.route('/')
def index():
    user = session.get('user')
    if not user:
        redirect(url_for('Pages.login'))
    return render_template('index.html', user=user)
