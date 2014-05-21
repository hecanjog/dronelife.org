from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import flash

from dronelife import app
from dronelife import db
from dronelife.models import User
from flask.ext.login import login_user
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])

@app.login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.data['username']).first()
        login_user(user)
        flash('Howdy!')

        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', form=form)
