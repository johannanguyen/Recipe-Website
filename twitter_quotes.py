from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import os

api_key = os.environ["API_KEY"]
api_secret_key = os.environ["API_SECRET_KEY"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret  = os.environ["ACCESS_TOKEN_SECRET"]
 
class listener(StreamListener):
    
    def on_data(self, data):

        tweet=data.split(',"text":"')[1].split('","source')[0]
        print(tweet+"\n")
        savefile=str(time.time())+"::"+tweet
        save=open('twitter_list.csv','a')
        save.write(savefile)
        save.write("\n\n")
        save.close()
        return True

    def on_error(self, status):
        print (status)
 
auth = OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
 
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["pasta"])