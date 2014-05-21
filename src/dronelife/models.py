from dronelife import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    last_login = db.Column(db.DateTime)
    post_count = db.Column(db.Integer)
    website = db.Column(db.String(120))
    twitter = db.Column(db.String(120))
    facebook = db.Column(db.String(120))
    bandcamp = db.Column(db.String(120))
    soundcloud = db.Column(db.String(120))
    description = db.Column(db.Text)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password 

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
