from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask import abort

from dronelife import app
from dronelife import db
from dronelife.models import User, Thread, Post, Reply, Topic
from flask.ext.login import login_required, current_user, login_user, logout_user
from flask.ext.wtf import Form
from wtforms import TextAreaField, TextField, PasswordField, HiddenField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class NewThreadForm(Form):
    title = TextField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])

class NewPostForm(Form):
    thread_id = HiddenField('thread_id', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])

class NewReplyForm(Form):
    post_id = HiddenField('post_id', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])

class ProfileForm(Form):
    username = TextField('username', validators=[DataRequired()])
    email = TextField('email', validators=[DataRequired()])
    website = TextField('website', validators=[DataRequired()])
    twitter = TextField('twitter', validators=[DataRequired()])
    facebook = TextField('facebook', validators=[DataRequired()])
    bandcamp = TextField('bandcamp', validators=[DataRequired()])
    soundcloud = TextField('soundcloud', validators=[DataRequired()])


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

@app.route('/threads/<id>/<title>')
def thread(id, title):
    thread = Thread.query.filter_by(id=id).first_or_404()
    postform = NewPostForm()
    replyform = NewReplyForm()

    return render_template('thread.html', thread=thread, postform=postform, replyform=replyform)

@app.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = ProfileForm()

    return render_template('profile.html', user=user, form=form)

@app.route('/profile')
def profileRedirect():
    return redirect('/'+current_user.username)

@app.route('/')
def index():
    topics = Topic.query.all()
    form = NewThreadForm()

    return render_template('index.html', form=form, topics=topics)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/posts', methods=['POST'])
@login_required
def addPost():
    form = NewPostForm()
    thread = Thread.query.filter_by(id=form.data['thread_id']).first_or_404()
    print form.data

    post = Post(
        form.data['content'], 
        current_user.id, 
        form.data['thread_id']
    )

    print post

    db.session.add(post)
    db.session.commit()

    return redirect(thread.getUrl())

@app.route('/replies', methods=['POST'])
@login_required
def addReply():
    form = NewReplyForm()
    post = Post.query.filter_by(id=form.data['post_id']).first_or_404()
    print form.data

    reply = Reply(
        form.data['content'], 
        current_user.id, 
        form.data['post_id']
    )

    db.session.add(reply)
    db.session.commit()

    thread = Thread.query.filter_by(id=post.thread_id).first_or_404()

    return redirect(thread.getUrl())


@app.route('/threads', methods=['POST'])
@login_required
def addThread():
    form = NewThreadForm()
    print form.data

    topic = Topic.query.filter_by(id=1).first_or_404()

    thread = Thread(
        form.data['title'], 
        form.data['content'], 
        current_user.id, 
        topic
    )

    db.session.add(thread)
    db.session.commit()

    thread = Thread.query.filter_by(title=thread.title).first_or_404()

    return redirect(thread.getUrl())

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
