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

    tweet = make_short_limerick()

    api.update_status(tweet)

def make_short_limerick():
    poet = Poet()

    limerick = poet.compose_limerick()

    final = ''
    for raw_line in limerick[:-1]:
        line = ' '.join(raw_line)
        final += line[0].upper() + line[1:] + '\n'
    line = ' '.join(limerick[-1])
    final += line[0].upper() + line[1:] + '\n'

    while len(final) > 140:
        limerick = poet.compose_limerick()

        final = ''
        for raw_line in limerick[:-1]:
            line = ' '.join(raw_line)
            final += line[0].upper() + line[1:] + '\n'
        line = ' '.join(limerick[-1])
        final += line[0].upper() + line[1:]

    return final

if __name__ == '__main__':
    tweet()