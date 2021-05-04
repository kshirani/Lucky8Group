# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT

import bcrypt
from flask import render_template, Flask  # Flask is the web app that we will customize
from flask import request
from flask import redirect,url_for

from database import db
from models import Event as Event

from models import User as User
from forms import RegisterForm, editAccount
from flask import session
from forms import LoginForm
from models import Comment as Comment
from models import Friendship as Friendship
from models import RSVP as RSVP

from forms import RegisterForm, LoginForm, RSVPForm, CommentForm


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


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/home')
def home():
    # retrieve user from database
    # check if a user is saved in session
    if session.get('user'):
        events = db.session.query(Event).all()
        # users = db.session.query(User).all

        # find the rsvps associated with the user id
        # rsvps = db.session.query(Rsvp).filter_by(user_id=session(['user_id'])).all()

        # find the events in rsvps
        # rsvp_events = db.session.query(Event).filter_by(event_id=rsvps.event_id).all()

        # rsvp = db.session.query(Rsvp).get(Rsvp.event_id).filter_by(user_id=session['user_id']).all()
        my_events = db.session.query(Event).filter_by(user_id=session['user_id']).all()
        # (user)                                       .all
        event_rsvps = db.session.query(RSVP).filter_by(user_id=session['user_id']).all()

        return render_template('home.html', index=events, notes=my_events, user=session['user'], rsvps=event_rsvps)

    else:
           return redirect(url_for('login'))

    @app.route('/home/<event_id>/report', methods=['GET', 'POST'])
    def report(event_id):
        if session.get('user'):
            # Retrieve event from database and the amount of times it was reported
            reported_event = db.session.query(Event).filter_by(id=event_id).one()
            report_count = reported_event.report_count
            # Increment amount of times it has been reported by 1
            report_count = report_count + 1
            # update count for the event
            reported_event.report_count = report_count

            # update db
            db.session.add(reported_event)
            db.session.commit()

            # Delete event if it has been reported 3 times
            if report_count >= 3:
                # Delete the event
                db.session.delete(reported_event)
                db.session.commit()

                # Return to home page after event is deleted
                return redirect(url_for('home'))

            # Go to Report.html page
            return render_template("report.html", event=reported_event, user=session['user'])
        else:
            # User is not in session, redirect to login
            return redirect(url_for('login'))

@app.route('/account')
def get_account():
    #check if a user is saved in session
    if session.get('user'):
        account = db.session.query(User).filter_by(id=session['user_id']).one()
        return render_template("account.html", user=session['user'], account=account)
    return render_template("home.html")



@app.route('/events')
def get_events():
    if session.get('user'):
        my_events = db.session.query(Event).filter_by(user_id=session['user_id']).all()
                                  # (user)                                       .all
        event_rsvps = db.session.query(RSVP).filter_by(user_id=session['user_id']).all()
        print(event_rsvps)
        return render_template('events.html', notes=my_events, user=session['user'],rsvps=event_rsvps )

    else:
        return redirect(url_for('login'))


#add a route and function to handle requests to display this view.  Since the purpose of this route is to display
# the details of one event will still need to utilize our mock list of notes.
@app.route('/events/<int:event_id>')
def get_event(event_id):
    if session.get('user'):
        my_event = db.session.query(Event).filter_by(id=event_id, user_id=session['user_id']).one()
        form_comment = CommentForm()
        event_rsvps = db.session.query(RSVP).filter_by(event_id=event_id).all()
        form_rsvp  = RSVPForm()
        print(event_rsvps)

        return render_template('event.html', event=my_event, user=session['user'], form_comment=form_comment, form_rsvp=form_rsvp, rsvps=event_rsvps )
    else:
        return redirect(url_for('login'))

#Let's add a route and function to handle requests to display this view.
@app.route('/events/new', methods=['GET','POST'])
def new_event():
    if session.get('user'):
        if request.method == 'POST':

            title = request.form['title']
            #get event data
            text = request.form['eventText']
            #create date stamp
            from datetime import date
            date = request.form['date']
            #format date mm/dd/yyyy
            newEntry = Event(title, text, date, session['user_id'])
            db.session.add(newEntry)
            db.session.commit()

            return redirect(url_for('get_events'))
        else:
            return render_template('new.html', user=session['user'])
    else:
        return redirect(url_for('login'))



@app.route('/events/edit/<event_id>', methods=['GET', 'POST'])
def update_event(event_id):
    #check method used for request
    if session.get('user'):
        if request.method == 'POST':
        #get title data
            title = request.form['title']
        #get event data
            text = request.form['eventText']
            date = request.form['date']
            address = request.form['address']
            event = db.session.query(Event).filter_by(id=event_id).one()
        #update event data
            event.title=title
            event.text = text
            event.date = date
            event.address = address
        #update event in DB
            db.session.add(event)
            db.session.commit()

            return redirect(url_for('get_events'))
        else:
        #retrive event from data base:
            my_event = db.session.query(Event).filter_by(id=event_id).one()

            return render_template('new.html', event=my_event, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/events/delete/<event_id>', methods=['POST'])
def delete_event(event_id):
    if session.get('user'):
        # retrieve event from database
        my_event = db.session.query(Event).filter_by(id=event_id).one()
        db.session.delete(my_event)
        db.session.commit()

        return redirect(url_for('get_events'))
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
        return redirect(url_for('get_events'))

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
            return redirect(url_for('get_events'))

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

    return redirect(url_for('home'))


@app.route('/events/<event_id>/comment', methods=['POST'])
def new_comment(event_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(event_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_event', event_id=event_id))

    else:
        return redirect(url_for('login'))

@app.route('/events/<event_id>/rsvp', methods=['POST'])
def new_rsvp(event_id):
   if session.get('user'):
       rsvp_form = RSVPForm()
       # validate_on_submit only validates using POST
       if rsvp_form.validate_on_submit():
           new_rsvp= RSVP(event_id,session['user_id'] )
           db.session.add(new_rsvp)
           db.session.commit()

       return redirect(url_for('get_event', event_id=event_id))

   else:
       return redirect(url_for('login'))


@app.route('/events/friends')
def get_friends():
    if session.get('user'):
        users = db.session.query(User).all()
        my_friends = db.session.query(Friendship).filter_by(user_id = session['user_id']).all()

        return render_template('friends.html', users=users, user=session['user'],friends=my_friends )
    else:
        return redirect(url_for('login'))

@app.route('/events/<friend_id>/friends', methods=['POST'])
def friend_add(friend_id):
    if session.get('user'):
        new_friendship = Friendship(friend_id, session['user_id'])
        db.session.add(new_friendship)
        db.session.commit()
        return redirect(url_for('get_friends'))
    else:
        return redirect(url_for('login'))

#@app.route('/account/edit/<user_id>', methods=['GET', 'POST'])
#@login_required
#def edit_account(user_id):
 #   form = editAccount()
  #  if request.method == 'POST':
  #      print('check data and submit')
   # else:
    #    print('get data from db and add to form')
        
# having issues with a redirect thing where the account edit function is not updating 
@app.route('/account/edit/<user_id>', methods=['GET', 'POST'])
def edit_account(user_id):
    form = RegisterForm()
    #print(user_id)
    if session.get('user'):
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']

            #account = db.session.query(User).filter_by(id=user_id).one()
            user_id.first_name = first_name
            user_id.last_name = last_name
            user_id.email = email

            db.session.add(user_id)
            db.session.commit()

            #my_account = db.session.query(user_id).filter_by(id=user_id).one()
            return redirect(url_for('get_account'))
        else:
            #retrive from data base:
            my_account = db.session.query(User).filter_by(id=user_id).one()

        return render_template('register.html', account=my_account, user=session['user'])
    else:
        return redirect(url_for('login'))

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#  c
# http://127.0.0.1:5000/home
# http://127.0.0.1:5000/notes
#notes/new
# http://127.0.0.1:5000/notes/1  or notes/2

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.

