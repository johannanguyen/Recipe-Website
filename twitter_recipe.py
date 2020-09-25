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
spoon_api = os.environ["SPOON_API"]


#Authentication for Twitter API
auth = OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


#Grab 1 tweet using keyword
def get_tweet(auth, keyword):
    tweet_list = []
    for tweet in Cursor(auth_api.search, q=keyword, lang="en").items(3):
        tweet_individual = []
        tweet_individual.append(tweet.user.profile_image_url)
        tweet_individual.append(tweet.user.name)
        tweet_individual.append(tweet.user.screen_name)
        tweet_individual.append(tweet.text)
        tweet_individual.append(str(tweet.created_at))
        tweet_list.append(tweet_individual)
        
    return tweet_list
    
    
#Grab food information using keyword
def get_food(keyword):
    food_link = f"https://api.spoonacular.com/recipes/complexSearch?query={keyword}&apiKey={spoon_api}&number=1"
    food_data = requests.get(food_link)
    pack_food_data = food_data.json()
    
    food_object = pack_food_data["results"][0]
    food_list = []
    food_list.append(food_object["id"])
    food_list.append(food_object["title"])
    food_list.append(food_object["image"])

    return food_list
    

#Grab source data using keyword
def get_source_recipe(food_id):
    source_recipe_link = f"https://api.spoonacular.com/recipes/{food_id}/information?includeNutrition=false&apiKey={spoon_api}"
    source_recipe_data = requests.get(source_recipe_link)
    pack_source_recipe_data = source_recipe_data.json()
    
    source_recipe = []
    source_recipe.append(pack_source_recipe_data["sourceName"])
    source_recipe.append(pack_source_recipe_data["sourceUrl"])
    
    recipe_object = pack_source_recipe_data["extendedIngredients"]
    length = len(recipe_object)
    
    for i in range(0, length):
        source_recipe.append(recipe_object[i]["originalString"])
    
    return source_recipe


#Run the app
app = Flask(__name__)
@app.route("/")

def index():
    keywords = ["cheesecake", "banana pudding", "funnel cake",
                "ice cream", "sundae", "cookie", "elcair",
                "doughnut", "mango float", "tiramisu", "creme brulee",
                "smores", "churro", "baklava", "ice cream float",
                "gelato", "tart", "pie"]
            

#Generate the proper tweets, recipes
    selected_keyword = random.choice(keywords)
    tweet = get_tweet(auth_api, selected_keyword)
    food = get_food(selected_keyword)
    source_recipe = get_source_recipe(food[0])
    
    return render_template(
        "index.html",
        food = food,
        tweet = tweet,
        source_recipe = source_recipe,
        len = len(source_recipe)
        )
        
app.run(
    debug=True,
    port=int(os.getenv("PORT", 8080)),
    host=os.getenv("IP", "127.0.0.1")
)
