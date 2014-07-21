from flask.ext.wtf import Form
from wtforms import TextAreaField, TextField, PasswordField, HiddenField, SelectField
from wtforms.validators import InputRequired, Optional

class LoginForm(Form):
    username = TextField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

class RegisterForm(Form):
    username = TextField('username', validators=[InputRequired()])
    email = TextField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

class NewThreadForm(Form):
    title = TextField('Title', validators=[InputRequired()])
    content = TextAreaField('Body', validators=[InputRequired()])
    topic_id = SelectField('Topic', validators=[InputRequired()])

class NewPostForm(Form):
    thread_id = HiddenField('thread_id', validators=[InputRequired()])
    content = TextAreaField('content', validators=[InputRequired()])

class NewReplyForm(Form):
    post_id = HiddenField('post_id', validators=[InputRequired()])
    content = TextAreaField('content', validators=[InputRequired()])

class ProfileForm(Form):
    username = TextField('username', validators=[InputRequired()])
    email = TextField('email', validators=[InputRequired()])
    website = TextField('website', validators=[Optional()])
    description = TextAreaField('description', validators=[Optional()])
    twitter = TextField('twitter', validators=[Optional()])
    facebook = TextField('facebook', validators=[Optional()])
    bandcamp = TextField('bandcamp', validators=[Optional()])
    soundcloud = TextField('soundcloud', validators=[Optional()])

class PasswordResetRequestForm(Form):
    email = TextField('email', validators=[InputRequired()])

class PasswordResetForm(Form):
    password = PasswordField('password', validators=[InputRequired()])
