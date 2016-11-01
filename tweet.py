'''
Twitter Tweeter
===============
Twitter bot class for tweeting poetry to account @infinite_poetry

Usage:
------
    python3 tweet.py [<path to file>]
'''

import tweepy
import sys

from keys import *
from poetry import Poet

def tweet():
    auth = tweepy.OAuthHandler(consumerKey, consumerKeySecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(auth)

    poet = Poet()

    limerick = poet.compose_limerick()

    tweet = ''
    for raw_line in limerick:
        line = ' '.join(raw_line)
        tweet += line[0].upper() + line[1:] + '\n'

    api.update_status(tweet)

if __name__ == '__main__':
    tweet()