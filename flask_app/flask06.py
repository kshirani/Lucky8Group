# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT

import bcrypt
from flask import render_template, Flask  # Flask is the web app that we will customize
from flask import request
from flask import redirect,url_for

from database import db
from models import Note as Note
from models import User as User
from forms import RegisterForm
from flask import session
from forms import LoginForm

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context
#}

notes = {1:{'title': 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
             2: {'title': 'Second note', 'text': 'This is my second note', 'date': '10-2-2020'},
             3: {'title': 'Third note', 'text': 'This is my third note', 'date': '10-3-2020'}}

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page

@app.route('/index')
def index():
    #check if a user is saved in session
    if session.get('user'):
        return render_template("index.html", user=session['user'])
    return render_template("index.html")
#^^^^^^Here we added a variable (a_user) to store our mock user data and we passed that
# variable to our template view (index.html) with a label called user.

@app.route('/notes')
def get_notes():
    if session.get('user'):
        my_notes = db.session.query(Note).filter_by(user_id=session['user_id']).all()

        return render_template('notes.html', notes=my_notes, user=session['user'])
    else:
        return redirect(url_for('login'))


#add a route and function to handle requests to display this view.  Since the purpose of this route is to display
# the details of one note will still need to utilize our mock list of notes.
@app.route('/notes/<note_id>')
def get_note(note_id):
    a_user = db.session.query(User).filter_by(email='ljoffrer@uncc.edu').one()
    my_note = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note=my_note ,user=a_user)

#Let's add a route and function to handle requests to display this view.
@app.route('/notes/new', methods=['GET','POST'])
def new_note():
    if session.get('user'):
        if request.method == 'POST':

            title = request.form['title']
            #get note data
            text = request.form['noteText']
            #create date stamp
            from datetime import date
            today = date.today()
            #format date mm/dd/yyyy
            today = today.strftime("%m-%d-%Y")
            newEntry = Note(title, text, today, session['user_id'])
            db.session.add(newEntry)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            return render_template('new.html', user=session['user'])
    else:
        return redirect(url_for('login'))



@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    #check method used for request
    if session.get('user'):
        if request.method == 'POST':
        #get title data
            title = request.form['title']
        #get note data
            text = request.form['noteText']
            note = db.session.query(Note).filter_by(id=note_id).one()
        #update note data
            note.title=title
            note.text = text
        #update note in DB
            db.session.add(note)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
        #retrive note from data base:
            my_note = db.session.query(Note).filter_by(id=note_id).one()

            return render_template('new.html', note=my_note, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    if session.get('user'):
        # retrieve note from database
        my_note = db.session.query(Note).filter_by(id=note_id).one()
        db.session.delete(my_note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        return redirect(url_for('login'))

#flask 6:
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_notes'))

    # something went wrong - display register view
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)
@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))



app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#  c
# http://127.0.0.1:5000/index
# http://127.0.0.1:5000/notes
#notes/new
# http://127.0.0.1:5000/notes/1  or notes/2

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
