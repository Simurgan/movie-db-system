from flask import Flask, render_template
from datetime import date

# Create a Flask Instance
app = Flask(__name__)

# Create a rouote decorator
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin/')
def sign_in():
    return render_template("signin.html")

@app.route('/admin/')
def admin():
    content = {
        "movieRating": {
            "movieID": 0,
            "movieName": "Inception",
            "overallRating": 4.5
        },
        "movies": {
            "director": "director1",
            "movieList": [
                {
                    "movieID": 0,
                    "movieName": "The Departed",
                    "theatreID": 5,
                    "district": "New York",
                    "timeSlot": 2
                },
                {
                    "movieID": 4,
                    "movieName": "The Wolf of The Wall Street",
                    "theatreID": 7,
                    "district": "Arizona",
                    "timeSlot": 3
                },
                {
                    "movieID": 9,
                    "movieName": "Goodfellas",
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
                    "rating": 4.9
                },
                {
                    "movieID": 1,
                    "movieName": "Pulp Fiction",
                    "rating": 4.9
                },
                {
                    "movieID": 2,
                    "movieName": "Django: Unchained",
                    "rating": 4.8
                }
            ]
        },
        "directorList": [
            {
                "username": "director1",
                "name": "director_name1",
                "surname": "director_surname1",
                "nation": "director_nationality1",
                "platform_id": "director_platformid1"
            },
            {
                "username": "director2",
                "name": "director_name2",
                "surname": "director_surname2",
                "nation": "director_nationality2",
                "platform_id": "director_platformid2"
            },
            {
                "username": "director3",
                "name": "director_name3",
                "surname": "director_surname3",
                "nation": "director_nationality3",
                "platform_id": "director_platformid3"
            }
        ]
    }
    return render_template("admin.html", content=content)


@app.route('/director/')
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