from dronelife import db
from datetime import datetime
from flask.ext.bcrypt import Bcrypt
import random
from dronelife import app
import urllib
from markdown import markdown
from dronelife.emoji import EmojiExtension

bcrypt = Bcrypt(app)

def parse_raw(content):
    return markdown(content, safe_mode=False, extensions=[EmojiExtension(), 'footnotes', 'sane_lists', 'tables', 'linkify'])

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120))
    created = db.Column(db.DateTime)

    def __init__(self, content):
        self.content = content 
        self.posted = datetime.utcnow()

    def __repr__(self):
        return '<Topic %s>' % self.content

    def getUrl(self):
        return '/topics/%s/%s' % (self.id, urllib.quote_plus(self.content))

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    raw_content = db.Column(db.Text)
    content = db.Column(db.Text)
    posted = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('thread'))
    locked = db.Column(db.Boolean)
    flagged = db.Column(db.Boolean)
    posts = db.relationship('Post', backref=db.backref('thread'), lazy='dynamic')

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship('Topic', backref=db.backref('threads', lazy='dynamic'))

    def __init__(self, title, content, author_id, topic, locked=False, flagged=False):
        self.title = title
        self.raw_content = content
        self.content = parse_raw(content)
        self.posted = datetime.utcnow()
        self.author_id = author_id
        self.topic = topic
        self.locked = locked
        self.flagged = flagged

    def __repr__(self):
        return '<Thread %s>' % self.title

    def setContent(self, content):
        self.raw_content = content
        self.content = parse_raw(content)
        self.edited = datetime.utcnow()

    def setTitle(self, title):
        self.title = title
        self.edited = datetime.utcnow()

    def getUrl(self):
        return '/threads/%s/%s' % (self.id, urllib.quote_plus(self.title))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_content = db.Column(db.Text)
    content = db.Column(db.Text)
    posted = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('post'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    replies = db.relationship('Reply', backref=db.backref('post'), lazy='dynamic')

    def __init__(self, content, author_id, thread_id):
        self.raw_content = content
        self.content = parse_raw(content) 
        self.posted = datetime.utcnow()
        self.author_id = author_id
        self.thread_id = thread_id

    def __repr__(self):
        return '<Post %s>' % self.raw_content

    def setContent(self, content):
        self.raw_content = content
        self.content = parse_raw(content)
        self.edited = datetime.utcnow()

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_content = db.Column(db.Text)
    content = db.Column(db.Text)
    posted = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, content, author_id, post_id):
        self.raw_content = content
        self.content = parse_raw(content)
        self.posted = datetime.utcnow()
        self.author_id = author_id
        self.post_id = post_id

    def __repr__(self):
        return '<Reply %s>' % self.raw_content

    def setContent(self, content):
        self.raw_content = content
        self.content = parse_raw(content)
        self.edited = datetime.utcnow()

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
    token = db.Column(db.String(120))
    token_expires = db.Column(db.DateTime)

    flagged = db.Column(db.Boolean)
    locked = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)
    is_moderator = db.Column(db.Boolean)

    threads = db.relationship('Thread', backref=db.backref('user'))
    posts = db.relationship('Post', backref=db.backref('user'))
    replies = db.relationship('Reply', backref=db.backref('user'))

    def __init__(self, username, email, password, is_admin=False, is_moderator=False):
        self.username = username
        self.email = email
        self.salt = bcrypt.generate_password_hash(random.random())
        self.password = bcrypt.generate_password_hash(password + self.salt)
        self.registered_on = datetime.utcnow()
        self.is_admin = is_admin
        self.is_moderator = is_moderator

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
        return bcrypt.check_password_hash(str(self.password), password + self.salt)
