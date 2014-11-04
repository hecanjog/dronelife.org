from flask.ext.script import Manager

from dronelife import app, twitter

manager = Manager(app)

@manager.command
def get_tweets():
    for tweet in twitter.api.search(q='thisisdronelife', result_type='recent'):
        print tweet.text

if __name__ == "__main__":
    manager.run()
