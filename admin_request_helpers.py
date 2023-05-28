def add_new_user(data):
  # db things
  print("add_new_user triggered")
  resp = {
    "feedback_to": "add-new-user",
    "status": "success"
  }

  return resp

def delete_audience(data):
  #db things
  print("delete_audience triggered")
  resp = {
    "feedback_to": "delete-audience",
    "status": "success"
  }

  return resp

def update_director_platform(data):
  #db things
  print("update-director-platform triggered")
  resp = {
    "feedback_to": "update-director-platform",
    "status": "success"
  }

  return resp

def view_average_rating(data):
  #db things
  print("view-average-rating triggered")
  resp = {
    "feedback_to": "view-average-rating",
    "status": "success"
  }

  return resp

def list_user_ratings(data):
  #db things
  print("list-user-ratings triggered")
  resp = {
    "feedback_to": "list-user-ratings",
    "status": "success"
  }

  return resp

def list_director_movies(data):
  #db things
  print("list-director-movies triggered")
  resp = {
    "feedback_to": "list-director-movies",
    "status": "success"
  }

  return resp

def list_directors(data):
  #db things
  print("list-directors triggered")
  resp = {
    "feedback_to": "list-directors",
    "status": "success"
  }

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
