# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import render_template, Flask  # Flask is the web app that we will customize
from flask import request

app = Flask(__name__)     # create an app

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page

@app.route('/index')
def index():
    a_user = {'name': 'Litzy', 'email':'mogli@uncc.edu'}
    return render_template('index.html' , user = a_user)
#^^^^^^Here we added a variable (a_user) to store our mock user data and we passed that
# variable to our template view (index.html) with a label called user.

@app.route('/notes')
def get_notes():
    a_user = {'name': 'Litzy', 'email':'mogli@uncc.edu'}
    notes = {1:{'title': 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
             2: {'title': 'Second note', 'text': 'This is my second note', 'date': '10-2-2020'},
             3: {'title': 'Third note', 'text': 'This is my third note', 'date': '10-3-2020'}}
    return render_template('notes.html', notes=notes, user=a_user)

#add a route and function to handle requests to display this view.  Since the purpose of this route is to display
# the details of one note will still need to utilize our mock list of notes.
@app.route('/notes/<note_id>')
def get_note(note_id):
    a_user = {'name': 'Litzy', 'email':'mogli@uncc.edu'}
    notes = {1:{'title': 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
             2: {'title': 'Second note', 'text': 'This is my second note', 'date': '10-2-2020'},
             3: {'title': 'Third note', 'text': 'This is my third note', 'date': '10-3-2020'}}
    return render_template('note.html', note=notes[int(note_id)],user=a_user)

#Let's add a route and function to handle requests to display this view.
@app.route('/notes/new', methods=['GET','POST'])
def new_note():
    #create mock user:
    a_user = {'name': 'Litzy', 'email':'mogli@uncc.edu'}

    #check method used for request
    print('request method is',request.method)
    if request.method == 'POST':
        return '<h1> POST method used for this request </h1>'
    else:
        return render_template('new.html', user=a_user)

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#  c
# http://127.0.0.1:5000/index
# http://127.0.0.1:5000/notes
# http://127.0.0.1:5000/notes/1  or notes/2

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.

