from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import os

api_key = os.environ["API_KEY"]
api_secret_key = os.environ["API_SECRET_KEY"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret  = os.environ["ACCESS_TOKEN_SECRET"]
        
class my_listener(StreamListener):
    def __init__(self, fetched_tweets):
        self.fetched_tweets = fetched_tweets
        
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets, "a") as ft:
                ft.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        
class TwitterStreamer():
    def stream_tweets(self, fetched_tweets, keywords):
        listener = my_listener(fetched_tweets)
        auth = OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
 
        twitterStream = Stream(auth, listener)
        twitterStream.filter(track=["pasta"])
 
if __name__ == "__main__":
    keywords = ["pasta"]
    fetched_tweets = "tweets.json"
    
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets, keywords)
    