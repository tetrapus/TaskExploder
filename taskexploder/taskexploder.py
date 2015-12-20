from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, g

from .api import blueprint as api_blueprint
from .pages import blueprint as pages_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_envvar('TASKEXPLODER_CONFIG', silent=True)
app.register_blueprint(api_blueprint)
app.register_blueprint(pages_blueprint)

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
