from dronelife import db
from dronelife.models import User

test_user = User('test', 'test@example.com', 'such-a-stong-password')

db.create_all()
db.session.add(test_user)
db.session.commit()

