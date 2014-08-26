from flask import Flask
from flask_appconfig.env import from_envvars
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager 
import os
import logging

login_manager = LoginManager()

app = Flask(__name__)

# Load app config info from environment variables
from_envvars(app.config, prefix=app.name.upper() + '_')

login_manager.init_app(app)

db = SQLAlchemy(app)

log_handler = logging.FileHandler(os.path.expanduser('~/dronelife.flask.log'))
log_handler.setLevel(logging.WARNING)
app.logger.addHandler(log_handler)

import admin_controller 
import controller
