from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import os
import spoon

api_key = os.environ["API_KEY"]
api_secret_key = os.environ["API_SECRET_KEY"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret  = os.environ["ACCESS_TOKEN_SECRET"]

"""
class TWITTER_CLIENT():
    def __init__(self):
        self.auth = AUTHENTICATOR().authenticate()
        self.twitter_client = API(self.auth)

    def get_tweets(self, num_tweets):
        tweets_list = []
        for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
            tweets_list.append(tweet)
        return tweets_list
"""

#Authenticate here, then return the auth object        
class AUTHENTICATOR():
    
    def authenticate(self):
        auth = OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        return auth
   

#Creates the stream
class TWITTER_STREAMER():
    
    def __init__(self):
        self.twitter_authenticator = AUTHENTICATOR()
        
    def stream_tweets(self, fetched_tweets, keywords):
        listener = MY_LISTENER(fetched_tweets)
        auth = self.twitter_authenticator.authenticate()
 
        twitterStream = Stream(auth, listener)
        twitterStream.filter(track=[keywords], languages=["en"])
        
        
class MY_LISTENER(StreamListener):
    def __init__(self, fetched_tweets, num_tweets = 0):
        self.fetched_tweets = fetched_tweets
        self.num_tweets = num_tweets
        
    def on_data(self, data):
        try:
            if self.num_tweets < 1:
                print(data)
                with open(self.fetched_tweets, "a") as ft:
                    ft.write(data)
                self.num_tweets +=1 
                return True
            else:
                return False
                
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            return False
        print(status)
        
 
if __name__ == "__main__":
    keywords = "chicken"
    fetched_tweets = "tweets.json"

    #twitter_client = TWITTER_CLIENT()
    #print(twitter_client.get_tweets(1))
    twitter_streamer = TWITTER_STREAMER()
    twitter_streamer.stream_tweets(fetched_tweets, keywords)
    