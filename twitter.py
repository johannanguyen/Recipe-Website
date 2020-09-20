"""

Successfully pull recipe data from Spoonacular

Variables that start with:
api - Deals with API and corresponding link
j   - Pulled from JSON file
h   - Used in HTML file

"""

import json
from flask import Flask, render_template #so we don't need to add "flask.Flask, flask.render_template
import os
import requests
import random

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

#Gather keys for API use
api_key = os.environ["API_KEY"]
api_secret_key = os.environ["API_SECRET_KEY"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret  = os.environ["ACCESS_TOKEN_SECRET"]

#Authentication for Twitter API
auth = OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth, wait_on_rate_limit=True)

#Grab tweets using keyword
def get_tweet(auth, keywords):
    tweet_list = []
    count = 1
    for tweet in Cursor(auth_api.search, q=keywords,lang="en").items(count):
        tweet_list.append(tweet.user.profile_image_url)
        tweet_list.append(tweet.user.name)
        tweet_list.append(tweet.user.screen_name)
        #tweet_list += tweet.text
        #tweet_list += str(tweet.created_at)
        tweet_list.append(tweet.text)
        tweet_list.append(str(tweet.created_at))
        
    return tweet_list
    
keywords = ["chicken", "ice cream", "pasta", "steak",
            "popcorn", "taco", "burrito", "salad",
            "sandwich", "bacon", "salmon", "burger",
            "cheesecake", "tres leches"]
            
selected_keyword = random.choice(keywords)
tweets = get_tweet(auth_api, selected_keyword)

app = Flask(__name__)
@app.route("/")


def index():
    return render_template(
        "index.html",
        hTweets = tweets)
        
app.run(
    debug=True,
    port=int(os.getenv("PORT", 8080)),
    host=os.getenv("IP", "127.0.0.1")
)
