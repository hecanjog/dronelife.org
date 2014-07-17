import MySQLdb
from dronelife import db, models
from datetime import datetime
from postmarkup import render_bbcode as bb
import HTMLParser
import re
from markdown import markdown
from dronelife.bbcode import BBCExtension

h = HTMLParser.HTMLParser()

topics = {
    9: ('Visual', 'visual'),
    8: ('Sound', 'shop talk'),
    7: ('DRONELIFE', 'the drone life'),
    6: ('Forums', 'the drone life'),
    10: ('Promotion', 'releases & promo'),
}

def frombb(content, guid=None):
    if guid is not None:
        content = content.replace(':%s' % guid, '') # remove guid injections from bbcode

    content = h.unescape(content) # decode html entities
    content = re.sub(r'<\!--*.+-->', '', content) # strip phpbb's html vomit
    content = content.replace(':%s' % guid, '') # remove guid injections from bbcode
    content = bb(content, paragraphs=True, render_unknown_tags=False)

    return content

con = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dronelife-legacy', use_unicode=True)

c = con.cursor()

c.execute('select * from phpbb_users where user_posts > 0')

users = []

for row in c:
    user = {
        'username': row[8].replace(' ', '_'),
        'email': row[12],
        'website': row[67],
        'description': frombb(row[58], row[59]),
        'registered_on': row[6], # int timestamp
        'id': row[0]
    }

    users += [ user ]

for userd in users:
    user = models.User.query.filter_by(email=userd['email']).first()
    if not user:
        user = models.User(userd['username'], userd['email'], '')

    if user.website != '':
        user.website = userd['website']

    user.description = userd['description']

    user.registered_on = datetime.utcfromtimestamp(int(userd['registered_on']))

    db.session.add(user)
    db.session.commit()
    print 'added %s' % user.username

threads = []

c.execute('select * from phpbb_topics')

for row in c:
    thread = {
        'title': row[6],
        'posted': row[8],
        'post_id': row[15],
        'author_id': row[7],
        'id': row[0],
        'topic_id': row[1]
    }

    threads += [ thread ]

#db.session.execute('truncate reply, post, thread')
db.session.commit()

for threadd in threads:


    # get topic
    topic = models.Topic.query.filter_by(content=topics[threadd['topic_id']][1]).first()
    if not topic:
        topic = models.Topic(topics[threadd['topic_id']][1])
        db.session.add(topic)
        db.session.commit()

    # get author_id
    c.execute('select user_email from phpbb_users where user_id = %s', [threadd['author_id']])
    author = models.User.query.filter_by(email=c.fetchone()[0]).first()

    # get post content
    c.execute('select post_text, bbcode_uid from phpbb_posts where post_id = %s', [threadd['post_id']])
    first_post = c.fetchone()

    content = frombb(first_post[0], first_post[1])

    title = h.unescape(threadd['title']) # decode html entities

    thread = models.Thread(title, content, author.id, topic)
    thread.posted = datetime.utcfromtimestamp(int(threadd['posted']))

    print title, topic, author
    db.session.add(thread)
    db.session.commit()

    posts = []
    c.execute('select topic_id, poster_id, post_time, post_text, bbcode_uid from phpbb_posts where topic_id = %s and post_id != %s', [threadd['id'], threadd['post_id']])

    for row in c:
        post = {
            'topic_id': row[0],
            'author_id': row[1],
            'posted': row[2],
            'content': row[3],
            'guid': row[4]
        }

        posts += [ post ]

    for postd in posts:
        # get author_id
        c.execute('select user_email from phpbb_users where user_id = %s', [postd['author_id']])
        r = c.fetchone()
        author = models.User.query.filter_by(email=r[0]).first()

        if author:
            content = frombb(postd['content'], postd['guid'])
            post = models.Post(content, author.id, thread.id)
            post.posted = datetime.utcfromtimestamp(int(postd['posted']))
            db.session.add(post)
            db.session.commit()

db.session.commit()

