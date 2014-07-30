from flask import Flask, render_template, redirect, request, url_for, flash, abort, session, jsonify
from flask.ext.login import login_required, current_user, login_user, logout_user
from dronelife import app, db, forms, models
from jinja2 import Environment
import random
#import mailchimp
import boto.ses as ses
from datetime import datetime

@app.before_request
def inject_bgimg():
    session['bgimg'] = random.choice([
        'elaine1.png', 
        'elaine2.png', 
        'elaine3.png', 
        'pauline1.png', 
        'ellen1.png', 
        'young.png'
    ])

@app.login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=int(user_id)).first()

@app.route('/users/username_exists')
def username_exists():
    username = request.args['username']
    user = models.User.query.filter_by(username=username).first_or_404()
    return jsonify({'exists': True})

@app.route('/users/email_exists')
def email_exists():
    email = request.args['email']
    user = models.User.query.filter_by(email=email).first_or_404()
    return jsonify({'exists': True})

@app.route('/password/reset/request', methods=['GET', 'POST'])
def password_reset_request():
    form = forms.PasswordResetRequestForm()
    if form.validate_on_submit():
        # set token
        user = models.User.query.filter_by(email=form.data['email']).first_or_404()
        token = user.set_token()
        db.session.commit()

        # send email
        c = ses.connect_to_region('us-east-1', 
            aws_access_key_id=app.config['AWS_KEY'],
            aws_secret_access_key=app.config['AWS_SECRET'])

        c.send_email('bot@dronelife.org', '[DRONELIFE] Password Reset Request', 
               """Heyo, 

Head over here to choose a new password: %spassword/reset/%s

If you didn't ask me to send this, just ignore it and the link will expire in an hour.

Love,

#dronebot
               """ % (request.url_root, token)
            , [form.data['email']])

    return render_template('password_reset_request.html', form=form)

@app.route('/password/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    user = models.User.query.filter_by(token=token).one()

    if not user or user.token_expires <= datetime.utcnow():
       abort(404) 

    form = forms.PasswordResetForm()

    if form.validate_on_submit():
        user.token_expires = datetime.utcnow()
        user.set_password(form.data['password']) 
        db.session.commit()
        return redirect('/login')

    return render_template('password_reset.html', token=token, form=form)

@app.route('/threads/<id>/<title>/')
def thread(id, title):
    thread = models.Thread.query.filter_by(id=id).first_or_404()
    postform = forms.NewPostForm()
    replyform = forms.NewReplyForm()

    return render_template('thread.html', thread=thread, postform=postform, replyform=replyform)

@app.route('/<username>')
def profile(username):
    user = models.User.query.filter_by(username=username).first_or_404()
    form = forms.ProfileForm()

    print form.description

    return render_template('profile.html', user=user, form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profileRedirect():
    form = forms.ProfileForm()

    if form.validate_on_submit():
        # update profile
        user = models.User.query.filter_by(username=form.data['username']).first()
        for attr, value in form.data.iteritems():
            setattr(user, attr, value)

        db.session.commit()
    else:
        print form.errors

    return redirect('/'+current_user.username)

@app.route('/')
def index():
    form = forms.NewThreadForm()
    first_threads = db.aliased(models.Thread)
    topics = models.Topic.query.all()
    form.topic_id.choices = [ (topic.id, topic.content) for topic in topics ]

    recent_users = models.User.query.order_by('registered_on desc').limit(20)

    posts = models.Post.query.order_by('posted desc').limit(5)
    threads = models.Thread.query.order_by('updated desc').limit(30)

    return render_template('index.html', 
            form=form, 
            topics=topics, 
            threads=threads, 
            posts=posts, 
            recent_users=recent_users
        )

@app.route('/topics/<id>/<title>')
def topic(id, title):
    form = forms.NewThreadForm()
    first_threads = db.aliased(models.Thread)
    topics = models.Topic.query.all()
    form.topic_id.choices = [ (topic.id, topic.content) for topic in topics ]

    topic = models.Topic.query.filter_by(id=id).one()

    return render_template('topic.html', form=form, topic=topic)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/posts', methods=['POST'])
@login_required
def addPost():
    form = forms.NewPostForm()
    thread = models.Thread.query.filter_by(id=form.data['thread_id']).first_or_404()
    print form.data

    post = models.Post(
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
    form = forms.NewReplyForm()
    post = models.Post.query.filter_by(id=form.data['post_id']).first_or_404()
    print form.data

    reply = models.Reply(
        form.data['content'], 
        current_user.id, 
        form.data['post_id']
    )

    db.session.add(reply)
    db.session.commit()

    thread = models.Thread.query.filter_by(id=post.thread_id).first_or_404()

    return redirect(thread.getUrl())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect('/')

    form = forms.RegisterForm() 

    if form.validate_on_submit():
        user = models.User(
            form.data['username'],
            form.data['email'],
            form.data['password']
        )

        db.session.add(user)
        db.session.commit()

        user = models.User.query.filter_by(username=form.data['username']).first()

        login_user(user)

        return redirect('/profile')

    return render_template('register.html', form=form)

@app.route('/threads', methods=['POST'])
@login_required
def addThread():
    form = forms.NewThreadForm()
    print form.data

    topic = models.Topic.query.filter_by(id=form.data['topic_id']).first()

    thread = models.Thread(
        form.data['title'], 
        form.data['content'], 
        current_user.id, 
        topic
    )

    db.session.add(thread)
    db.session.commit()

    thread = models.Thread.query.filter_by(title=thread.title).first_or_404()

    return redirect(thread.getUrl())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.data['username']).first()
        if user is not None and user.check_hash(form.data['password']) == True:
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()

            flash('Welcome back!', 'info')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Passwords are the worst. Give\'er another try.', 'warning')

    return render_template('login.html', form=form)
