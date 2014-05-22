from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask import abort

from dronelife import app
from dronelife import db
from dronelife.models import User
from flask.ext.login import login_required, current_user, login_user, logout_user
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

@app.login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

@app.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    return render_template('profile.html', user=user)

@app.route('/')
def index():
    user = load_user(1)
    return render_template('index.html', user=user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.data['username']).first()
        if user is not None and user.check_hash(form.data['password']) == True:
            login_user(user)
            flash('Howdy!')

            return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', form=form)
