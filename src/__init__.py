import os
from flask import Blueprint
from flask_session import Session

app_blueprint = Blueprint(os.environ["app_name"], __name__)