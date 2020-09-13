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

app = Flask(__name__)
@app.route("/")

def index():
    
    #Opens API link
    
    apiLink = "https://api.spoonacular.com/recipes/random&number=1"
    apiData = requests.get(apiLink)

    #Places API data in a usable package
    pack_apiData = apiData.json()

    #Sets each desired attribute using JSON
    jOverview = pack_apiData["recipes"][0]
    jTitle = jOverview["title"]
    jKeyword = jTitle.split()[0].strip()
    jImage = jOverview["image"]
    jURL = jOverview["sourceUrl"]

    return render_template(
        "index.html",
        hTitle = jTitle,
        hImage = jImage,
        hURL = jURL,
        hKeyword = jKeyword)

app.run(
    debug=True,
    port=int(os.getenv("PORT", 8080)),
    host=os.getenv("IP", "127.0.0.1")
)
