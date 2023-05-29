import mysql.connector

class database:
  def __init__(self):
    self.db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password123",
      database="movie_db"
    )

    self.cursor = self.db.cursor()

  def execute(self, query):
    try:
      self.cursor.execute(query)
      return self.cursor.fetchall()
    except Exception as ex:
      print("execute error:")
      print(ex)
      return False

  def save(self):
    try:
      self.db.commit()
      return True
    except:
      print("save error")
      return False

  def close(self):
    self.cursor.close()
    self.db.close()