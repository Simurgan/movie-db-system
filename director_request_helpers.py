from db import database

def add_new_movie(data, username):
    # db things
    db = database()

    movieID = data.get('movieID')
    movieName = data.get('movieName')
    theatreID = data.get('theatreID')
    timeSlot = data.get('timeSlot')

    query = 'INSERT INTO Movies (movieID, movieName, timeSlot, averageRating, numOfRatings, directorUserName, theatreID) VALUES ("' + movieID + '", "' + movieName + '", "' + timeSlot + '", "' + "0" + '", "' + "0" + '", "' + username + '", ' + theatreID +")"

    e_check = db.execute(query)
    s_check = db.save()

    status = "Success"

  

    if not ((not e_check == False) and s_check):
        status = "Fail"

    resp = {
    "feedback_to": "add_new_movie",
    "status": status,
    "data": None
    }

    db.close()
    return resp

def add_predecessor(data, username):
    #db things
    db = database()

    movieID = data.get('movieID')
    predecessorMovieID = data.get('predecessorMovieID')

    query = "INSERT INTO Preceedings (movieID, predecessorMovieID) VALUES ('" + movieID + "', '" + predecessorMovieID +"')"

    e_check = db.execute(query)
    s_check = db.save()

    status = "Success"

  

    if not ((not e_check == False) and s_check):
        status = "Fail"

    resp = {
    "feedback_to": "add_predecessor",
    "status": status,
    "data": None
    }

    db.close()
    return resp

def update_movie_name(data, username):
    #db things
    db = database()

    movieID = data.get('movieID')
    newMovieName = data.get('newMovieName')
    
    query = 'UPDATE Movies SET movieName = "' + newMovieName + '" WHERE movieID =' + movieID 

    e_check = db.execute(query)
    s_check = db.save()

    status = "Success"

  

    if not ((not e_check == False) and s_check):
        status = "Fail"

    resp = {
    "feedback_to": "update_movie_name",
    "status": status,
    "data": None
    }

    db.close()
    return resp

def list_available_theatres(data, username):
    #db things
    db = database()
    status = "Success"
    slot = data.get('slot')

    all_t_query = "SELECT theatreID, theatreDistrict, theatreCapacity FROM theatres"
    all_ts = db.execute(all_t_query)

    busy_t_query = "SELECT T.theatreID FROM Theatres T INNER JOIN Movies M ON T.theatreID = M.theatreID WHERE M.timeSlot = " + slot
    busy_ts = db.execute(busy_t_query)

    submit = []
    for t in all_ts:
        check = True
        for o in busy_ts:
            if t[0] == o[0]:
                check = False
        
        if check:
            submit.append(t)

    if not submit:
        status = "Fail: no available slots or another internal error"

    resp = {
        "feedback_to": "add_new_movie",
        "status": status,
        "data": {
            "field": "availableTheatres",
            "data": submit
        }
    }

    db.close()
    return resp

def list_my_movies(data, username):
    #db things
    db = database()


    query = "SELECT movieID, movieName, theatreID, timeSlot FROM Movies WHERE directorUserName ='" + username + "'"

    movieDatas = db.execute(query)
    s_check = db.save()

    status = "Success"

    directorsMovies=[]

    if not ((not movieDatas == False) and s_check):
        status = "Fail"

    else:
        for movieData in movieDatas:
            theatre_query = "SELECT predecessorMovieID FROM Preceedings WHERE movieID = " + str(movieData[0])
            predecessorsData = db.execute(theatre_query)
            s_check = db.save()

            predecessorsList = ""
            if predecessorsData:
                for predecessor in predecessorsData:
                    predecessorsList += str(predecessor[0]) + ", "
            

            movieData = list(movieData)
            movieData.append(predecessorsList)
            directorsMovies.append(movieData)



    resp = {
        "feedback_to": "add_new_movie",
        "status": status,
        "data": {
            "field": "directorsMovies",
            "data": directorsMovies
        }
    }

    db.close()
    return resp

def list_movie_audiences(data, username):
  #db things
    db = database()
    movieID = data.get('movieID')

    query = "SELECT * FROM Movies WHERE movieID =" + movieID + " AND directorUserName = '" + username + "'"

    isDirectorsMovie = db.execute(query)
    s_check = db.save()

    movieAudiences=[]

    if isDirectorsMovie:

        movieID_query = "SELECT sessionID FROM MovieSessions WHERE movieID ='" + movieID + "'"

        movieSessionDatas = db.execute(movieID_query)
        s_check = db.save()

        status = "Success"

        

        if not ((not movieSessionDatas == False) and s_check):
            status = "Fail"

        else:
            for movieSession in movieSessionDatas:
                session_query = "SELECT userName FROM Attendances WHERE sessionID = " + str(movieSession[0])
                sessionData = db.execute(session_query)
                s_check = db.save()

                if not ((not sessionData == False) and s_check):
                    status = "Fail"

                for audiences in sessionData:
                    audiences_query = 'SELECT userName, name, surname FROM Users WHERE userName = "' + str(audiences[0]) + '"'
                    audiencesData = db.execute(audiences_query)
                    s_check = db.save()

                    if not ((not audiencesData == False) and s_check):
                        status = "Fail"

                    movieAudiences.append(audiencesData[0])
    else:
        status = "Fail"


    resp = {
        "feedback_to": "list_movie_audiences",
        "status": status,
        "data": {
            "field": "movieAudiences",
            "data": movieAudiences
        }
    }

    db.close()
    return resp



handlers = {
    "add-new-movie": add_new_movie,
    "add-predecessor": add_predecessor,
    "update-movie-name": update_movie_name,
    "list-available-theatres": list_available_theatres,
    "list-my-movies": list_my_movies,
    "list-movie-audiences": list_movie_audiences
}

def handle_director_request(data, username):
    return handlers[data.get('form_name')](data, username)
