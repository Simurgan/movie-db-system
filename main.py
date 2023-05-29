from flask import Flask, render_template, request, redirect, session
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
from admin_request_helpers import handle_request
from director_request_helpers import handle_director_request
from audience_request_helpers import handle_audience_request
from db import database

# Create a Flask Instance
app = Flask(__name__)
app.secret_key = 'secret_key'

# Create a rouote decorator

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        return login()
    else:
        return render_template("signin.html")
    
@app.route('/signout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    content = {
        "data": {
            "movieRating": None,
            "movies": None,
            "userRating": None,
            "directorsList": None
        },
        "feedbacks": {
            "add_new_user": "",
            "delete_audience": "",
            "update_director_platform": "",
            "view_average_rating": "",
            "list_user_ratings": "",
            "list_director_movies": "",
            "list_directors": ""
        }
    }

    if request.method == 'POST':
        response = handle_request(request.form)

        content["feedbacks"][response["feedback_to"]] = response["status"]
        if response["data"]:
            content["data"][response["data"]["field"]] = response["data"]["data"]
        
    return render_template("admin.html", content=content)

@app.route('/director/', methods=['GET', 'POST'])
def director():
    content = {
        "data": {
            "availableTheatres": None,
            "directorsMovies": None,
            "movieAudiences": None
        },
        "feedbacks": {
            "add_new_movie": "",
            "add_predecessor": "",
            "update_movie_name": "",
            "list_available_theatres": "",
            "list_my_movies": "",
            "list_movie_audiences": ""
        }
    }

    if request.method == 'POST':
        response = handle_director_request(request.form, session["username"])

        content["feedbacks"][response["feedback_to"]] = response["status"]
        if response["data"]:
            content["data"][response["data"]["field"]] = response["data"]["data"]
        
    return render_template("director.html", content=content)




@app.route('/audience/', methods=['GET', 'POST'])
def audience():
    content = {
        "data": {
            "movies": None,
            "userRating": None
        },
        "feedbacks": {
            "buy_a_ticket": "",
            "rate_movie": "",
            "list_movies": "",
            "list_bought_ticket": ""
        }
    }

    if request.method == 'POST':
        response = handle_audience_request(request.form, session["username"])

        content["feedbacks"][response["feedback_to"]] = response["status"]
        if response["data"]:
            content["data"][response["data"]["field"]] = response["data"]["data"]

    return render_template("audience.html", content=content)

@app.route('/instance_user_page/<name>')
def instance_user_page(name):
    return render_template("instance.html", name=name)

# some filters
# safe
# capitalize
# upper
# title
# trim
# striptags

def login():
    # Retrieve the username and password from the login form
    username = request.form.get('username')
    password = request.form.get('password')

    # Establish a connection to the MySQL database
    db = database()

    # Execute a SELECT query to retrieve the user with the given username and password
    user_query = "SELECT * FROM users WHERE userName = '" + username + "' AND password = '" + password + "'"
    user = db.execute(user_query)

    director_query = "SELECT * FROM directors WHERE username = '" + username + "'"
    director = db.execute(director_query)

    admin_query = "SELECT * FROM databasemanagers WHERE username = '" + username + "'  AND password = '" + password + "'"
    admin = db.execute(admin_query)

    # Close the cursor and database connection
    db.close()

    if admin:
        session['username'] = username
        return redirect('/admin')

    # Check if a user with the given username and password exists
    elif user and director:
        session['username'] = username
        # User exists, perform the login action (e.g., redirect to a dashboard)
        return redirect('/director') 
    elif user:
        session['username'] = username
        return redirect('/audience') 
    else:
        # User does not exist, display an error message
        return 'Invalid credentials'
