'''
Twitter Tweeter
===============
Twitter bot class for tweeting poetry to account @infinite_poetry

Usage:
------
    python3 tweet.py [<path to file>]
'''

import tweepy
import random

from keys import *
from poetry import Poet

import os
import sys

# Get py-verse directory
path = os.path.abspath(os.path.dirname(sys.argv[0]))

poet = Poet(path + '/data/english.txt')

def make_short_limerick():
    limerick = poet.compose_limerick()

    final_lim = make_poem(limerick)

    while len(final_lim) > 140:
        limerick = poet.compose_limerick()

        final_lim = make_poem(limerick)

    return final_lim

def make_short_haiku():
    haiku = poet.compose_haiku()

    final_haiku = make_poem(haiku)

    while len(final_haiku) > 140:
        haiku = poet.compose_haiku()

        final_haiku = make_poem(haiku)

    return final_haiku

def make_short_love_poem():
    love_poem = poet.compose_love_poem()

    while None in love_poem:
        love_poem = poet.compose_love_poem()

    final_love_poem = make_poem(love_poem)

    while len(final_love_poem) > 140:
        love_poem = poet.compose_love_poem()

        final_love_poem = make_poem(love_poem)

    return final_love_poem

def make_short_doublet():
    doublet = poet.compose_doublet()

    while None in doublet:
        doublet = poet.compose_doublet()

    final_doublet = make_poem(doublet)

    while len(final_doublet) > 140:
        doublet = poet.compose_doublet()

        final_doublet = make_poem(doublet)

    return final_doublet

def make_short_quatrain():
    quatrain = poet.compose_quatrain()

    final_quatrain = make_poem(quatrain)

    while len(final_quatrain) > 140:
        quatrain = poet.compose_quatrain()

        final_quatrain = make_poem(quatrain)

    return final_quatrain

def make_poem(poem):
    final = ''
    for raw_line in poem[:-1]:
        line = ' '.join(raw_line)
        final += line[0].upper() + line[1:] + '\n'
    line = ' '.join(poem[-1])
    final += line[0].upper() + line[1:]

    return final

def tweet():
    auth = tweepy.OAuthHandler(consumerKey, consumerKeySecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(auth)

    poetry_methods = [
    make_short_limerick, 
    make_short_haiku, 
    make_short_love_poem, 
    make_short_doublet,
    make_short_quatrain]

    random_poem = random.choice(poetry_methods)

    tweet = random_poem()

    # api.update_status(tweet)
    print(tweet)

if __name__ == '__main__':
    tweet()