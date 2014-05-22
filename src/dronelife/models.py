from dronelife import db
from datetime import datetime
from flask.ext.bcrypt import Bcrypt
import random
from dronelife import app

bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    salt = db.Column(db.String(120))
    last_login = db.Column(db.DateTime)
    post_count = db.Column(db.Integer)
    website = db.Column(db.String(120))
    twitter = db.Column(db.String(120))
    facebook = db.Column(db.String(120))
    bandcamp = db.Column(db.String(120))
    soundcloud = db.Column(db.String(120))
    description = db.Column(db.Text)
    registered_on = db.Column(db.DateTime)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.salt = bcrypt.generate_password_hash(random.random())
        self.password = bcrypt.generate_password_hash(password + self.salt)
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password + self.salt)
