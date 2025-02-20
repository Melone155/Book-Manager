import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="mydatabase"
)

def ConnectDataBase():
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Buecher BuchID AUTO_INCREMENT, Titel VARCHAR(50), ErscheinungsJahr DATA")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Benutzer BenutzerID AUTO_INCREMENT, Vorname VARCHAR(100), Nachnamen VARCHAR(100), Email VARCHAR(255)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS  Ausleihen AusleiID AUTO_INCREMENT, BenutzerID VARCHAR(255), BuchID VARCHAR(255)")