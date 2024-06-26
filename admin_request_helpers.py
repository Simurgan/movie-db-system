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
  ret_data = None
  status = "Success"

  db = database()

  query = "SELECT M.movieID, M.movieName, M.theatreID, T.theatreDistrict, M.timeSlot FROM movies M INNER JOIN theatres T ON M.theatreID = T.theatreID WHERE M.directorUserName = '" + username + "'"
  rec = db.execute(query)

  if not rec:
    status = "Fail: no movies directed by this director or another internal error"
  else:
    ret_data = {
      "field": "movies",
      "data": {
        "director": username,
        "movieList": []
      }
    }

    for movie in rec:
      ret_data["data"]["movieList"].append({
        "movieID": movie[0],
        "movieName": movie[1],
        "theatreID": movie[2],
        "district": movie[3],
        "timeSlot": movie[4]
      })

  resp = {
    "feedback_to": "list_director_movies",
    "status": status,
    "data": ret_data
  }

  return resp

def list_directors(data):
  status = "Success"
  ret_data = None

  db = database()

  query = "SELECT U.userName, U.name, U.surname, D.nationality, D.platformID  FROM Directors D INNER JOIN Users U ON D.userName = U.userName"
  directors = db.execute(query)

  if not directors:
    status = "Fail: no director record or internal error"
  else:
    ret_data = {
      "field": "directorList",
      "data": []
    }

    for dir in directors:
      ret_data["data"].append({
        "username": dir[0],
        "name": dir[1],
        "surname": dir[2],
        "nation": dir[3],
        "platform_id": dir[4]
      })

  resp = {
    "feedback_to": "list_directors",
    "status": status,
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
