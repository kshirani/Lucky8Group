# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import render_template, Flask  # Flask is the web app that we will customize

app = Flask(__name__)     # create an app

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page

@app.route('/index')
def index():
    a_user = {'name': 'Litzy', 'email':'mogli@uncc.edu'}
    return render_template('index.html' , user = a_user)
#Here we added a variable (a_user) to store our mock user data and we passed that
# variable to our template view (index.html) with a label called user.

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#  c
# http://127.0.0.1:5000/index !!

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
