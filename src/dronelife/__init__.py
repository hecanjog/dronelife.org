from flask import Flask
from flask_appconfig.env import from_envvars
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load app config info from environment variables
from_envvars(app.config, prefix=app.name.upper() + '_')

db = SQLAlchemy(app)

from dronelife import controller
