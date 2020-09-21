# project1-jn354

This website displays recipe information and tweets of a randomly selected dish.

In order to use this repository:
0. Sign up for a Twitter developer account at: https://developer.twitter.com
1. Create a new app: https://developer.twitter.com/en/portal/projects-and-apps
2. Click on the key icon to display your keys
3. Sign up for a Spoonacular account at: https://spoonacular.com/food-api/console#Dashboard
4. Confirm your Spoonacular account using the corresponding email address
5. Retrive your Spoonacular API key by clicking "Profile" in the left margin
6. Clone this repository
7. Install tweepy by running the following in your terminal (depending on which version of pip you are using):
    sudo pip install tweepy -or-
    sudo pip3 install tweepy
8. Install flask by running the following in your terminal (depending on which version of pip you are using):
    sudo pip install flask -or-
    sudo pip3 install flask
9. Install python-dotenv by running the following in your terminal (depending on which version of pip you are using):
    sudo pip install python-dotenv -or-
    sudo pip3 install python-dotenv
10. Create a root-level .env file and add your keys as follows:
    export ACCESS_TOKEN=""
    export ACCESS_TOKEN_SECRET=""
    export API_KEY=""
    export API_SECRET_KEY=""
    export SPOONACULAR_API=""
11. Source your .env file by running the following in your terminal:
    source [filename].env
12. Execute the program by running the following in your terminal:
    python twitter_recipe.py
    
<img src="https://i.ibb.co/KWBdnyY/p1m1.png">
