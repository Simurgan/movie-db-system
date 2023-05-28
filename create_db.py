#Standard library import
import mysql.connector

#Connect with the precise info, also with dataset name
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd = "password123",
  	database="our_users"
)

#Command needed to modify/access inside database(s)
mycursor = mydb.cursor()

#Execute SQL Script
mycursor.execute("SELECT name, address FROM bellooo")

#Obtain all rows with fetchall
myresult = mycursor.fetchall()

#Print the results
for x in myresult:
  print(x)