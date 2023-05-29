from flask import Flask, render_template, request, redirect
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
from admin_request_helpers import handle_request
from db import database

# Create a Flask Instance
app = Flask(__name__)

# Create a rouote decorator

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        return login()
    else:
        return render_template("signin.html")

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
        "movieAudiences": {
            "movieID": 7,
            "movieName": "Yandım Ali: Son Osmanlı",
            "audiences": [
                {
                    "username": "crazy_boy_80",
                    "name": "Ömer Şükrü",
                    "surname": "Uyduran"
                },
                {
                    "username": "banker_bilo_27",
                    "name": "Bilal",
                    "surname": "Atım"
                }
            ]
        },
        "availableTheatres": {
            "date": date.today(),
            "slot": 1,
            "theatres": [
                {
                    "theatreID": 7,
                    "district": "Arizona",
                    "capacity": 100
                },
                {
                    "theatreID": 3,
                    "district": "Los Angeles",
                    "capacity": 60
                }, 
                {
                    "theatreID": 2,
                    "district": "Hollywood",
                    "capacity": 40
                }
            ]
        },
        "directorsMovies": [
            {
                "movieID": 9,
                "movieName": "Ice Age 3",
                "theatreID": 9,
                "date": date.today(),
                "timeSlot": 1,
                "predecessors": "Ice Age 2, Ice Age 1"
            },
            {
                "movieID": 7,
                "movieName": "Shrek 3",
                "theatreID": 4,
                "date": date.today(),
                "timeSlot": 2,
                "predecessors": "Shrek 2, Shrek 1"
            },
            {
                "movieID": 1,
                "movieName": "John Wick 3",
                "theatreID": 54,
                "date": date.today(),
                "timeSlot": 3,
                "predecessors": "John Wick 2, John Wick 1"
            }
        ]
    }
    return render_template("director.html", content=content)




@app.route('/audience/', methods=['GET', 'POST'])
def audience():
    input_data = request.form.get('sessionID')
    print(input_data)
    content = {
        "movies": {
            "director": "director1",
            "movieList": [
                {
                    "movieID": 0,
                    "movieName": input_data,
                    "directorUsername": "kyle.balda",
                    "platform": "Netflix",
                    "predecessorsList": "Bumerang Cehennemi, Deli Yürek",
                    "theatreID": 5,
                    "district": "New York",
                    "timeSlot": 2
                },
                {
                    "movieID": 4,
                    "movieName": "The Wolf of The Wall Street",
                    "directorUsername": "kyle.balda",
                    "platform": "Netflix",
                    "predecessorsList": "Bumerang Cehennemi, Deli Yürek",
                    "theatreID": 7,
                    "district": "Arizona",
                    "timeSlot": 3
                },
                {
                    "movieID": 9,
                    "movieName": "Goodfellas",
                    "directorUsername": "kyle.balda",
                    "platform": "Netflix",
                    "predecessorsList": "Bumerang Cehennemi, Deli Yürek",
                    "theatreID": 9,
                    "district": "Coralado",
                    "timeSlot": 1
                }
            ]
        },
        "userRating": {
            "username": "audience_1",
            "ratings": [
                {
                    "movieID": 0,
                    "movieName": "Hateful Eight",
                    "rating": 4.3,
                    "sessionID": 12930,
                    "overallRating": 4.1
                },
                {
                    "movieID": 1,
                    "movieName": "Pulp Fiction",
                    "rating": "",
                    "sessionID": 12400,
                    "overallRating": 4
                },
                {
                    "movieID": 2,
                    "movieName": "Django: Unchained",
                    "rating": 4.8,
                    "sessionID": 12530,
                    "overallRating": 4.3
                }
            ]
        },
        
    }
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
        return redirect('/admin')

    # Check if a user with the given username and password exists
    elif user and director:
        # User exists, perform the login action (e.g., redirect to a dashboard)
        return redirect('/director') 
    elif user:
         return redirect('/audience') 
    else:
        # User does not exist, display an error message
        return 'Invalid credentials'
"""

@app.route('/add-user', methods=['GET', 'POST'])
def addNewUser():
    if request.method == 'POST':
        # Retrieve the username and password from the registration form
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        surname = request.form.get('surname')

                # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='your_host',
            user='your_username',
            password='your_password',
            database='your_database'
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        query = "INSERT INTO users (username, password, namei surname) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, password, name, surname))
        
        type = request.form.get('type')
        if type=="director":
            nationality = request.form.get('nationality')
            platformID = request.form.get('platformID')

            query = "INSERT INTO directors (username, nationality, platformID) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, nationality, platformID))

        else:
            query = "INSERT INTO audiences (username) VALUES (%s)"
            cursor.execute(query, (username))

        # Commit the transaction and close the cursor and database connection
        connection.commit()
        cursor.close()
        connection.close()

        # Display a success message or redirect the user to a success page
        return 'Registration successful'

    else:
        return render_template('admin.html')

"""