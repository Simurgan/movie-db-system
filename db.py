import mysql.connector

class database:
  def __init__(self):
    self.db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd = "password123",
      database="movie_db"
    )

    self.cursor = self.db.cursor()

  def execute(self, query, params):
    self.cursor.execute(query, params)
    return self.cursor.fetchone()

  def close(self):
    self.cursor.close()
    self.db.close()