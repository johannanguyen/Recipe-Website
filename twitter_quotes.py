import tweepy
from twitter_credentials import *

#Create a StreamListener
class my_listener(tweepy.StreamListener):
    
    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True
        
    def process_data(self, raw_data):
        print(raw_data)

    def on_error(self, status_code):
        if status_code == 420:
            return False
            
#Create a Stream
class my_stream():
    
    def __init__(self, auth, listener):
        
        #Doesn't do anything with the stream, only makes it
        self.stream = tweepy.Stream(auth=auth, listener=listener)
        
    def start(self, keyword_list):
        
        #Track can be anything you want to search Tweets for
        self.stream.filter(track="keyword_list")

#Start the stream
if __name__ == "__main__":
    
    listener = my_listener()
    
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    stream = my_stream(auth, listener)
    stream.start(["ice cream"])