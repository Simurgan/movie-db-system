from db import database

def add_new_user(data):
  # db things
  db = database()

  username = data.get('username')
  password = data.get('password')
  name = data.get('name')
  surname = data.get('surname')
  user_type = data.get('user-type')

  query = "INSERT INTO Users (userName, password, name, surname) VALUES ('" + username + "', '" + password + "', '" + name + "', '" + surname + "')"

  e_check = db.execute(query)
  s_check = db.save()

  status = "Success"

  if (not e_check == False) and s_check:
    if user_type == "director":
      nation = data.get('nation')
      platformID = data.get('platformID')
      
      query = "INSERT INTO Directors (userName, nationality, platformID) VALUES ('" + username + "', '" + nation + "', " + platformID + ")"

      e_check = db.execute(query)
      s_check = db.save()

      if not ((not e_check == False) and s_check):
        status = "Fail"

      # sub = username + " " + password + " " + name + " " + surname + " " + user_type + " " + nation + " " + platformID
    else:
      query = "INSERT INTO Audiences (userName) VALUES ('" + username + "')"

      e_check = db.execute(query)
      s_check = db.save()

      if not ((not e_check == False) and s_check):
        status = "Fail"

      # sub = username + " " + password + " " + name + " " + surname + " " + user_type
  else:
    status = "Fail"

  resp = {
    "feedback_to": "add_new_user",
    "status": status,
    "data": None
  }

  db.close()
  return resp

def delete_audience(data):
  #db things
  username = data.get('username')
  
  resp = {
    "feedback_to": "delete_audience",
    "status": username,
    "data": None
  }

  return resp

def update_director_platform(data):
  #db things
  username = data.get('username')
  platform_ID = data.get('platform_ID')

  query = username + " " + platform_ID
  
  resp = {
    "feedback_to": "update_director_platform",
    "status": query,
    "data": None
  }

  return resp

def view_average_rating(data):
  #db things
  
  movie_ID = data.get('movie_ID')

  ret_data = {
    "field": "movieRating",
    "data": {
      "movieID": movie_ID,
      "movieName": "Inception",
      "overallRating": 4.5
    }
  }
  
  resp = {
    "feedback_to": "view_average_rating",
    "status": "Success!",
    "data": ret_data
  }

  return resp

def list_user_ratings(data):
  #db things

  username = data.get('username')

  ret_data = {
    "field": "userRating",
    "data": {
      "username": username,
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
    }
  }

  resp = {
    "feedback_to": "list_user_ratings",
    "status": "success",
    "data": ret_data
  }

  return resp

def list_director_movies(data):
  #db things

  username = data.get('username')
  
  ret_data = {
    "field": "movies",
    "data": {
      "director": username,
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
    }
  }

  resp = {
    "feedback_to": "list_director_movies",
    "status": "success",
    "data": ret_data
  }

  return resp

def list_directors(data):
  #db things

  ret_data = {
    "field": "directorList",
    "data": [
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

  resp = {
    "feedback_to": "list_directors",
    "status": "success",
    "data": ret_data
  }

  return resp

handlers = {
  "add-new-user": add_new_user,
  "delete-audience": delete_audience,
  "update-director-platform": update_director_platform,
  "view-average-rating": view_average_rating,
  "list-user-ratings": list_user_ratings,
  "list-director-movies": list_director_movies,
  "list-directors": list_directors
}

def handle_request(data):
  return handlers[data.get('form_name')](data)
