from flask import Blueprint
from . import accounts
from . import tasks


blueprint = Blueprint("API", __name__, url_prefix="/api")
accounts.register(blueprint)
tasks.register(blueprint)