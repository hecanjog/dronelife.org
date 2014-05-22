from dronelife import db
from dronelife.models import User
from dronelife.models import Topic
from dronelife.models import Thread
from dronelife.models import Post
from dronelife.models import Reply

test_user = User('test', 'test@example.com', 'password')
db.session.add(test_user)
test_topic = Topic('dronelife')
db.session.add(test_topic)
test_thread = Thread('test', 'foo', test_user.id, test_topic)
db.session.add(test_thread)

db.create_all()
db.session.commit()

