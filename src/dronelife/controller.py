from flask import Flask
from flask import render_template
from dronelife import app
from dronelife import db
from dronelife.models import User

@app.route('/')
def index():
    return render_template('index.html')

