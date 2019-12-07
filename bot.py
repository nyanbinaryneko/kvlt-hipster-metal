import tweepy
import os
from poser_takes import generate_poser_take

DEBUG = os.environ["DEBUG"].lower() == "true"
sentence = generate_poser_take()
print(f'bot - finished sentence: {sentence}')
if not DEBUG:
    CONSUMER_API = os.environ["CONSUMER_API_KEY"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_SECRET = os.environ["ACCESS_SECRET"]

    auth = tweepy.OAuthHandler(CONSUMER_API, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(sentence)
    print(f'bot - status updated')