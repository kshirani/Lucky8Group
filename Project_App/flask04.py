# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import render_template, Flask  # Flask is the web app that we will customize
from flask import request
from flask import redirect,url_for

#flask04.py:{
from database import db
from models import Event as Event
from models import User as User

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context
#}


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page

@app.route('/home')
def home():
    #get user from database
    a_user =  db.session.query(User).filter_by(email='ljoffrer@uncc.edu').one()

    return render_template('home.html' , user = a_user)
#^^^^^^Here we added a variable (a_user) to store our mock user data and we passed that
# variable to our template view (index.html) with a label called user.

@app.route('/events')
def get_events():
    #retrieve user from database
    a_user = db.session.query(User).filter_by(email='ljoffrer@uncc.edu').one()
    #retrieve notes from database:
    my_events = db.session.query(Event).all()

    return render_template('events.html', notes=my_events, user=a_user)

#add a route and function to handle requests to display this view.  Since the purpose of this route is to display
# the details of one note will still need to utilize our mock list of notes.
@app.route('/events/<event_id>')
def get_event(event_id):
    a_user = db.session.query(User).filter_by(email='ljoffrer@uncc.edu').one()
    my_event = db.session.query(Event).filter_by(id=event_id).one()

    return render_template('event.html', event=my_event ,user=a_user)

#Let's add a route and function to handle requests to display this view.
@app.route('/events/new', methods=['GET','POST'])
def new_event():
    #adding commits after directory error

    #check method used for request
    if request.method == 'POST':
        #get title data
        title = request.form['title']
        #get event data
        text = request.form['eventText']
        #create date stamp
        from datetime import date
        today = date.today()
        #format date mm/dd/yyyy
        today = today.strftime("%m-%d-%Y")
        newEntry = Event(title, text, today)
        db.session.add(newEntry)
        db.session.commit()

        return redirect(url_for('get_events'))
    else:
        a_user = db.session.query(User).filter_by(email='ljoffrer@uncc.edu').one()
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

