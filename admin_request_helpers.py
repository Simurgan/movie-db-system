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
  username = data.get('username')

  db = database()

  # check if audience exist

  query_check = "SELECT * FROM audiences WHERE userName = '" + username + "'"
  rec = db.execute(query_check)


  status = "Success"
  if not rec:
    status = "Fail: no such audience"
  else:
    query_admin = "DELETE FROM Users WHERE userName = '" + username + "'"
    query_audience = "DELETE FROM Audiences WHERE userName = '" + username + "'"

    check_ae = db.execute(query_admin)
    check_as = db.save()

    check_ue = db.execute(query_audience)
    check_us = db.save()

    if check_ae == False or (not check_as) or check_ue == False or (not check_us):
      status = "Failed to delete audience"
  
  resp = {
    "feedback_to": "delete_audience",
    "status": status,
    "data": None
  }

  return resp

def update_director_platform(data):
  username = data.get('username')
  platform_ID = data.get('platform_ID')

  status = "Success"
  db = database()

  # check if director exist
  query_check = "SELECT * FROM directors WHERE userName = '" + username + "'"
  rec = db.execute(query_check)
  if not rec:
    status = "Fail: no such director"
  else:
    query = "UPDATE directors SET platformID = " + platform_ID + " WHERE userName = '" + username + "'"
    e_check = db.execute(query)
    s_check = db.save()

    if e_check == False or (not s_check):
      status = "Failed to update director platform"
    else:
      # update the movies
      m_query = "UPDATE movies SET directorPlatformID = " + platform_ID + " WHERE directorUserName = '" + username + "'"
      me_check = db.execute(m_query)
      ms_check = db.save()

      if me_check == False or (not ms_check):
        status = "Failed to update movies of the director even though update of itself was successful!"

  resp = {
    "feedback_to": "update_director_platform",
    "status": status,
    "data": None
  }

  return resp

def view_average_rating(data):
  movie_ID = data.get('movie_ID')
  
  status = "Success"
  ret_data = None

  db = database()

  # check if movie exists
  query_check = "SELECT * FROM movies WHERE movieID = " + movie_ID
  rec = db.execute(query_check)
  if not rec:
    status = "Fail: no such movie or another internal error"
  else:
    ret_data = {
      "field": "movieRating",
      "data": {
        "movieID": rec[0][0],
        "movieName": rec[0][1],
        "overallRating": rec[0][3]
      }
    }
  
  resp = {
    "feedback_to": "view_average_rating",
    "status": status,
    "data": ret_data
  }

  return resp

def list_user_ratings(data):
  username = data.get('username')

  status = "Success"
  ret_data = None

  db = database()

  # check if audience exists
  query_check = "SELECT * FROM audiences WHERE userName = '" + username + "'"
  rec = db.execute(query_check)
  if not rec:
    status = "Fail: no such audience or another internal error"
  else:
    # check if ratings exist
    ratings_query = "SELECT movieID, rating FROM ratings WHERE userName = '" + username + "'"
    ratings = db.execute(ratings_query)
    if not ratings:
      status = "Fail: this audience has no ratings"
    else:
      ret_data = {
        "field": "userRating",
        "data": {
          "username": username,
          "ratings": []
        }
      }
      for rec in ratings:
        # get movieName
        m_name_query = "SELECT movieName FROM movies WHERE movieID = " + str(rec[0])
        m_n_res = db.execute(m_name_query)
        if not m_n_res:
          status = "Fail: internal error"
        else:
          ret_data["data"]["ratings"].append({
            "movieID": rec[0],
            "movieName": m_n_res[0][0],
            "rating": rec[1]
          })

  resp = {
    "feedback_to": "list_user_ratings",
    "status": status,
    "data": ret_data
  }

  return resp

def list_director_movies(data):
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
