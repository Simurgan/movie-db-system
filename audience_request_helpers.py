from db import database

def buy_a_ticket(data, username):
    # db things
    db = database()

    sessionID = data.get('sessionID')
    predecessor_query = 'SELECT P.predecessorMovieID FROM Preceedings P INNER JOIN MovieSessions MS INNER JOIN Movies M ON MS.movieID = M.movieID AND MS.movieID = P.movieID WHERE MS.sessionID =' + str(sessionID)
    predecessor_data = db.execute(predecessor_query)
    s_check = db.save()


    attendances_query = 'SELECT M.movieID FROM attendances A INNER JOIN moviesessions M ON A.sessionID = M.sessionID WHERE userName = "' + username + '"'
    attendances_data = db.execute(attendances_query)
    s_check = db.save()

    isWatchAll = True

    for predicessor in predecessor_data:
        if predicessor not in attendances_data:
            isWatchAll = False

    if not (isWatchAll):
        status = "Audience don't watch all predicessors"

    else:


        buy_query = 'INSERT INTO Attendances (userName, sessionID) VALUES ("' + username + '", ' + sessionID +")"
        e_check = db.execute(buy_query)
        s_check = db.save()

        status = "Success"


    

        if not ((not e_check == False) and s_check):
            status = "Fail"

    resp = {
    "feedback_to": "buy_a_ticket",
    "status": status,
    "data": None
    }

    db.close()
    return resp

def rate_movie(data, username):
    #db things
    db = database()

    sessionID = data.get('sessionID')
    rate = data.get('rate')

    movieID_query = "SELECT movieID FROM MovieSessions WHERE sessionID = " + sessionID
    movieID_data = db.execute(movieID_query)
    s_check = db.save()

    rate_query = 'INSERT INTO Ratings (userName, movieID, rating) VALUES ("' + username + '", ' + str(movieID_data[0][0]) + "," + rate + ")"
    buy_data = db.execute(rate_query)
    s_check = db.save()

    print(rate_query)

    status = "Success"

  

    if not ((not buy_data == False) and s_check):
        status = "Fail"

    resp = {
    "feedback_to": "rate_movie",
    "status": status,
    "data": None
    }

    db.close()
    return resp


def list_movies(data, username):
    #db things
    db = database()


    query = "SELECT movieID, movieName, surname, platformName, theatreID, timeSlot FROM movies M INNER JOIN directors D INNER JOIN platforms P INNER JOIN users U ON M.directorUserName = D.userName AND P.platformID = D.platformID AND U.userName = D.userName"


    movieData = db.execute(query)
    s_check = db.save()

    status = "Success"

    movies=[]

    if not ((not movieData == False) and s_check):
        status = "Fail"

    else:
        for movie in movieData:
            predecessors_query = "SELECT predecessorMovieID FROM Preceedings WHERE movieID = " + str(movie[0])
            predecessorsData = db.execute(predecessors_query)
            s_check = db.save()

            predecessorsList = ""
            if predecessorsData:
                for predecessor in predecessorsData:
                    predecessorsList += str(predecessor[0]) + ", "
            

            movie = list(movie)
            movie.append(predecessorsList)
            movies.append(movie)



    resp = {
        "feedback_to": "list_movies",
        "status": status,
       "data": {
            "field": "movies",
            "data": movies
        }
    }

    db.close()
    return resp

def list_bought_ticket(data, username):
    #db things
    db = database()


    bought_and_rated_query = 'SELECT M.movieID, M.movieName, MS.sessionID, R.rating, M.averageRating FROM movies M INNER JOIN MovieSessions MS INNER JOIN attendances A INNER JOIN ratings R ON A.sessionID = MS.sessionID AND MS.movieID = M.movieID AND R.movieID = MS.movieID  AND A.userName = R.userName WHERE R.userName= "' + username + '"'

    boughtAndRatedData = db.execute(bought_and_rated_query)
    s_check = db.save()
    
    bought_query = 'SELECT M.movieID, M.movieName, MS.sessionID, M.averageRating, M.averageRating FROM movies M INNER JOIN MovieSessions MS INNER JOIN attendances A ON A.sessionID = MS.sessionID AND MS.movieID = M.movieID WHERE A.userName= "' + username + '"'

    boughtData = db.execute(bought_query)
    s_check = db.save()

    status = "Success"

    for i in range(len(boughtData)):
        boughtData[i] = list(boughtData[i])
        boughtData[i][3] = " "

    for i in range(len(boughtData)):
        for j in range(len(boughtAndRatedData)):
            if boughtData[i][0] == boughtAndRatedData[j][0]:
                boughtData[i][3] = boughtAndRatedData[j][3]
        
    print(boughtData)

    if not ((not boughtAndRatedData == False) and s_check):
        status = "Fail"

    resp = {
        "feedback_to": "list_bought_ticket",
        "status": status,
        "data": {
            "field": "userRating",
            "data": boughtData
        }
    }

    db.close()
    return resp



handlers = {
    "buy-a-ticket": buy_a_ticket,
    "rate-movie": rate_movie,
    "list-movies": list_movies,
    "list-bought-ticket": list_bought_ticket
    }

def handle_audience_request(data, username):
    return handlers[data.get('form_name')](data, username)
