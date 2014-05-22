from flask import Flask
from flask_appconfig.env import from_envvars
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager 

login_manager = LoginManager()

app = Flask(__name__)

# Load app config info from environment variables
from_envvars(app.config, prefix=app.name.upper() + '_')

login_manager.init_app(app)

db = SQLAlchemy(app)

from dronelife import controller
