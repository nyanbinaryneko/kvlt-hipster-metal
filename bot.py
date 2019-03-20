from markov import generate_genre
import time
import tweepy
import os
import markovify
import logging
import random

log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)

CONSUMER_API = os.environ["CONSUMER_API_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["ACCESS_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_API, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
genre = generate_genre(140) # half the tweet
STEMS = [f"Oh, you think you are kvlt, I only listen to {genre}.", f"if you were really into metal you would know {genre}.", f"Hey, poser, I'm the founder of {genre}.", f"These fuckin' kids never heard of {genre}.", f"I remember the days before hipsters and posers infecting {genre}.", f"{genre} IS FOR REAL METALHEADS ONLY!!!!", f'I was listening to {genre} before you were born.', f"you like {genre}? ugh. that's for posers."]
STEM = random.choice(STEMS)
if random.randint(0, 10) == 1:
    sentence = f'{STEM}'.upper()
else:
    sentence = f'{STEM}'
print(f'bot - finished sentence: {sentence}')
if "rac" in sentence.lower():
    sentence = f'{genre.upper()} IS FOR FUCKING POSERS. LISTEN TO REAL METAL YOU PANDA COSPLAYERS!'
api.update_status(sentence)