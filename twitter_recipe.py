import json
from flask import Flask, render_template
import os
import requests
import random
from tweepy.streaming import StreamListener
from tweepy import *


#Gather keys from .env for API use
api_key = os.environ["API_KEY"]
api_secret_key = os.environ["API_SECRET_KEY"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret  = os.environ["ACCESS_TOKEN_SECRET"]
spoon_api = os.environ["SPOON_API"]


#Authentication for Twitter API
auth = OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


#Grab 3 tweets using keyword
#Returns a list of lists
#Each individual list includes [image, author, screen name, tweet text, date created]
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
#Pulls up three food objects and randomly selects from one of those three
#Returns a list containing [id, title, image]
def get_food(keyword):
    food_link = f"https://api.spoonacular.com/recipes/complexSearch?query={keyword}&apiKey={spoon_api}&number=3"
    food_data = requests.get(food_link)
    pack_food_data = food_data.json()
    
    item_select = random.randint(0, 2)
    food_object = pack_food_data["results"][item_select]
    food_list = []
    food_list.append(food_object["id"])
    food_list.append(food_object["title"])
    food_list.append(food_object["image"])

    return food_list
    

#Grab source and recipe data using food id
#Returns a list containing [source name, source url, prep time, ingredient 1, ingredient 2, ... , ingredient length]
def get_source_recipe(food_id):
    source_recipe_link = f"https://api.spoonacular.com/recipes/{food_id}/information?includeNutrition=false&apiKey={spoon_api}"
    source_recipe_data = requests.get(source_recipe_link)
    pack_source_recipe_data = source_recipe_data.json()
    
    source_recipe = []
    source_recipe.append(pack_source_recipe_data["sourceName"])
    source_recipe.append(pack_source_recipe_data["sourceUrl"])
    source_recipe.append(pack_source_recipe_data["readyInMinutes"])
    
    recipe_object = pack_source_recipe_data["extendedIngredients"]
    length = len(recipe_object)
    
    for i in range(0, length):
        source_recipe.append(recipe_object[i]["originalString"])
    
    return source_recipe


#Run the app
app = Flask(__name__)
@app.route("/")

def index():
    
    #Randomly selects from one of these keywords
    keywords = ["cheesecake", "pudding", "ice cream", "sundae", 
                "cookie", "doughnut",  "tiramisu", "creme brulee",
                 "cake", "gelato", "tart", "pie", "custard", 
                 "tres leches", "jello", "sugar"]
            

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
