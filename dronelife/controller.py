from flask import Flask, render_template, redirect, request, url_for, flash, abort, session
from flask.ext.login import login_required, current_user, login_user, logout_user
from dronelife import app, db, forms, models
from jinja2 import Environment
import random

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

@app.route('/threads/<id>/<title>')
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
def profileRedirect():
    form = forms.ProfileForm()

    if form.validate_on_submit():
        # update profile
        user = models.User.query.filter_by(username=form.data['username']).first()
        print user.website
        for attr, value in form.data.iteritems():
            setattr(user, attr, value)

        db.session.commit()
    else:
        print form.errors

    return redirect('/'+current_user.username)

@app.route('/')
def index():
    form = forms.NewThreadForm()
    topics = models.Topic.query.all()
    form.topic_id.choices = [ (topic.id, topic.content) for topic in topics ]

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

            return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', form=form)
