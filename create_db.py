
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  auth_plugin='mysql_native_password',
  port=3306,
  database="moviedbdb"
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE moviedb")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
  print(db)
  