from markov import generate_genre
import time
import tweepy
import os
import markovify
import logging
import random
from metal_albumify import AlbumCover
import json

log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)

CONSUMER_API = os.environ["CONSUMER_API_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["ACCESS_SECRET"]

DEBUG = True

auth = tweepy.OAuthHandler(CONSUMER_API, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
if not DEBUG:
    genre = generate_genre(140) # half the tweet
    STEMS = [f"Oh, you think you are kvlt, I only listen to {genre}.", f"if you were really into metal you would know {genre}.", f"Hey, poser, I'm the founder of {genre}.", f"These fuckin' kids never heard of {genre}.", f"I remember the days before hipsters and posers infecting {genre}.", f"{genre} IS FOR REAL METALHEADS ONLY!!!!", f'I was listening to {genre} before you were born.', f"you like {genre}? ugh. that's for posers."]
    STEM = random.choice(STEMS)
    if random.randint(0, 10) == 1:
        sentence = f'{STEM}'.upper()
    else:
        sentence = f'{STEM}'
    print(f'bot - finished sentence: {sentence}')
    if "rac" in sentence.lower() or "oi!" in sentence.lower():
        sentence = f'{genre.upper()} IS FOR FUCKING POSERS. LISTEN TO REAL METAL YOU PANDA COSPLAYERS!'
    api.update_status(sentence)

# this is strictly to have it only annoy me while testing. Heroku branch will have this
# disabled and credit the author of the tweet for posting the pic.

if DEBUG:
    tweets = []
    for tweet in tweepy.Cursor(api.user_timeline, id="snepbot", tweet_mode='extended', exclude_replies=True).items(100):
        tweet.entities["media"] = [m for m in tweet.entities["media"] if m["type"] == "photo"]
        if(len(tweet.entities["media"]) > 0):
            tweets.append(tweet)
    tw = random.choice(tweets)
    # status = api.get_status(id="1175100612410839041")
    media = tw.entities["media"]
    cover = AlbumCover(media[0]["media_url_https"], './corpus/img/testlogo.png').paste_logo_image()
    api.update_with_media(filename=cover, status=f'henlo mxtress, here is that test for you: its from my friend here!!: {tw.extended_entities["media"][0]["expanded_url"]}' , in_reply_to_status_id="1175100612410839041",  auto_populate_reply_metadata=True)


