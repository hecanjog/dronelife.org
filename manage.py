from flask.ext.script import Manager

from dronelife import app, twitter

manager = Manager(app)

@manager.command
def get_tweets():
    for tweet in twitter.api.search(q='thisisdronelife', result_type='recent'):
        # check to see if this tweet is already a thread

        # check to see if the tweet author's handle matches any dronelife user's 
            # twitter handle set in the profile... better enforce @username style
            # data. Can prolly clean up existing data:
                # matches URL: strip username from URL, add @
                # matches @username: leave alone
                # matches neither of the above: prepend with @

            # if found, set correct author, otherwise --- set as 'twitter' user?

        # if not, create a new thread
        # category should be something special...
        # title & body of post are tweet.text

        print dir(tweet)
        print tweet.author.screen_name
        print tweet.id

if __name__ == "__main__":
    manager.run()
