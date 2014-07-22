import mailchimp
from dronelife import models, db, app

mc = mailchimp.Mailchimp(apikey=app.config['MAILCHIMP_APIKEY'])
lists = mailchimp.Lists(mc)
list_id = lists.list()['data'][0]['id']
users = models.User.query.all()
emails = [ {'email': {'email': user.email}} for user in users ]
lists.batch_subscribe(list_id, emails, double_optin=False)

