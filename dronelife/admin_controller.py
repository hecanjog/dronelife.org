from flask import redirect
from flask.ext.admin import Admin, AdminIndexView, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
from dronelife import app, models, db

class AdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect('/')
        elif not current_user.is_admin:
            return redirect('/')

        return super(AdminIndex, self).index()

class UserView(ModelView):
    column_list = ('username', 'email', 'last_login', 'post_count', 'registered_on', 'is_admin', 'is_moderator')

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(models.User, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_admin
        else:
            False

class TopicView(ModelView):
    def __init__(self, session, **kwargs):
        super(TopicView, self).__init__(models.Topic, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_admin
        else:
            False

class ThreadView(ModelView):
    def __init__(self, session, **kwargs):
        super(ThreadView, self).__init__(models.Thread, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_admin
        else:
            False

admin = Admin(app, 'Dronelife', index_view=AdminIndex())
admin.add_view(UserView(db.session))
admin.add_view(TopicView(db.session))
admin.add_view(ThreadView(db.session))
