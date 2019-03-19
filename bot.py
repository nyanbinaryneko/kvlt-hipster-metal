from markov import generate_genre
import time
import tweepy
import os
import markovify
import logging

log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)

CONSUMER_API = os.environ["CONSUMER_API_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["ACCESS_SECRET"]

STEM = "Oh, you think you are kvlt, I only listen to "
# STEMS = ["Oh, you think you are kvlt, I only listen to ", "if you were really into metal you would know ", "Hey, poser, I'm the founder of ", "These fuckin' kids never heard of ", "I remember the days before hipsters and posers infecting "], 
# MID = [f'I was listen to {genre} before you were born.', f"you like {genre}? ugh. that's for posers."]
# BASE = [" IS FOR REAL METALHEADS ONLY!!!!"]
auth = tweepy.OAuthHandler(CONSUMER_API, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

log.debug("generating sentence")
total = 280 - len(STEM)
sentence = f'{STEM}{generate_genre(total)}'
api.update_status(sentence)