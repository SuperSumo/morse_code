# References:
# https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py
# http://tweepy.readthedocs.org/en/v2.3.0/index.html
# http://stackoverflow.com/questions/870520/in-python-how-do-you-filter-a-string-such-that-only-characters-in-your-list-are
# http://stackoverflow.com/questions/1207457/convert-a-unicode-string-to-a-string-in-python-containing-extra-symbols

# Other libraries
from tweepy import StreamListener
from HTMLParser import HTMLParser
from pygame.mixer import pre_init
import json
import time
import tweepy
import logging
import pygame
import string

# My imports
from _auth import *
from morse import string_to_morse, play_morse, letterToMorse


class UserListener(StreamListener):

    def __init__(self, api, user):

        self._api = api
        self._user = user

    def filter_text(self, text):

        # I can only translate certain characters. Remove all others.
        chars = "".join(sorted([str(x) for x in letterToMorse.keys()]))
        deleteTable = string.maketrans(chars, "^" * len(chars))
        # Remove unicode encoding and apply the translation table
        return text.encode("ascii", "ignore").translate(None, deleteTable)

    def on_data(self, rawData):

        # Load the data from the json
        data = json.loads(HTMLParser().unescape(rawData))

        # If they tweeted mentioning the user with an @, translate it
        if "text" in data and "user" in data:
            if "@" + self._user in data["text"]:

                # Create a json object of the important parts I care about
                text = data["text"]  # The body of the message
                print "raw text:", text
                filtered = self.filter_text(text)
                print "filtered text:", filtered
                # The morse code representation
                morse = string_to_morse(filtered)
                tweet = {"text":        text,
                         "username":    data["user"]["name"],
                         "screenname":  data["user"]["screen_name"],
                         "when":        time.time(),
                         "morse":       morse}
                # Log the tweet
                logging.info(json.dumps(tweet))
                # Play the morse code on the speaker
                play_morse(morse)

    def on_error(self, statusCode):

        logging.error(statusCode)
        return False


def setup_logging():

    # Set up the root logger to a file
    logLevel = logging.DEBUG
    logFormat = "%(levelname)s:%(message)s"
    logging.basicConfig(filename=username + ".log",
                        format=logFormat,
                        level=logLevel)

    # Set up another logger to print to the screen
    console = logging.StreamHandler()
    console.setLevel(logLevel)
    formatter = logging.Formatter(logFormat)
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

if __name__ == "__main__":

    # Initialize pygame sound stuff
    pre_init(44100, -16, 1, 1024)
    pygame.init()

    # Whoever tweets to this username will be parsed
    username = "tweetmorsecode"

    # Set up logging
    setup_logging()

    # Set up a twitter listener
    listen = UserListener(api, username)

    # Set up a twitter stream handler
    stream = tweepy.Stream(auth, listen)

    print "Streaming started..."

    # Stream and log forever
    while(True):
        try:
            stream.userstream()
        except Exception, e:
            logging.error(e)
            stream.disconnect()
