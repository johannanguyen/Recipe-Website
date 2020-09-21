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
def get_source(food_id):
    source_link = f"https://api.spoonacular.com/recipes/{food_id}/information?includeNutrition=false&apiKey={spoon_api}"
    source_data = requests.get(source_link)
    pack_source_data = source_data.json()
    
    source_list = []
    source_list.append(pack_source_data["sourceName"])
    source_list.append(pack_source_data["sourceUrl"])
    
    return source_list
    
    
#Grab recipe information by food id
def get_recipe(food_id):
    recipe_link = f"https://api.spoonacular.com/recipes/{food_id}/information?includeNutrition=false&apiKey={spoon_api}"
    recipe_data = requests.get(recipe_link)
    pack_recipe_data = recipe_data.json()
    
    recipe_object = pack_recipe_data["extendedIngredients"]
    length = len(recipe_object)
    recipe_list = []
    
    for i in range(0, length):
        recipe_list.append(recipe_object[i]["originalString"])
    
    return recipe_list


#Run the app
app = Flask(__name__)
@app.route("/")

def index():
    keywords = ["chicken", "ice cream", "pasta", "steak",
            "popcorn", "taco", "burrito", "salad",
            "sandwich", "bacon", "salmon", "burger",
            "cheesecake", "tres leches", "beef stew",
            "pizza", "pineapple", "sushi"]
            

#Generate the proper tweets, recipes
    selected_keyword = random.choice(keywords)
    tweet = get_tweet(auth_api, selected_keyword)
    food = get_food(selected_keyword)
    recipe = get_recipe(food[0])
    source = get_source(food[0])
    
    return render_template(
        "index.html",
        len = len(recipe),
        food = food,
        recipe = recipe,
        tweet = tweet,
        source = source
        )
        
app.run(
    debug=True,
    port=int(os.getenv("PORT", 8080)),
    host=os.getenv("IP", "127.0.0.1")
)
