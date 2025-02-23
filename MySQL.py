import mysql.connector
import tkinter

import YML

def test_mysql_connection(host, port, user, password, database):
    """Testet die MySQL-Verbindung und zeigt eine Meldung an"""
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        CreateTable(conn)
        conn.close()
        YML.save_mysql_config(host, port, user, password, database)
        tkinter.messagebox.showinfo(title="Connect", message="Connection to database successful and Tables was Create")
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror(title="Error", message=f"Connection failed: {err}")

def CheckTabel(conn):
    mycursor = conn.cursor()
    mycursor.execute("SHOW TABLES LIKE 'Books'")


def CreateTable(conn):
    mycursor = conn.cursor()
    try:
        # Überprüfe, ob die Tabellen existieren
        mycursor.execute("SHOW TABLES LIKE 'Books'")
        resultBook = mycursor.fetchone()  # Gibt ein Tupel zurück, wenn die Tabelle existiert, sonst None

        mycursor.execute("SHOW TABLES LIKE 'User'")
        resultUser = mycursor.fetchone()

        mycursor.execute("SHOW TABLES LIKE 'Borrow'")
        resultBorrow = mycursor.fetchone()

        # Create Tables, wenn sie nicht existieren
        if not resultBook:
            mycursor.execute("CREATE TABLE IF NOT EXISTS Books (BookID INT AUTO_INCREMENT PRIMARY KEY, Title VARCHAR(50) NOT NULL, PublicationYear YEAR NOT NULL);")
        if not resultUser:
            mycursor.execute("CREATE TABLE IF NOT EXISTS User (UserID INT AUTO_INCREMENT PRIMARY KEY, FirstName VARCHAR(100) NOT NULL, LastName VARCHAR(100) NOT NULL, Email VARCHAR(255) UNIQUE NOT NULL, Permission VARCHAR(5) NOT NULL, Passwort VARCHAR(255) NOT NULL)")
        if not resultBorrow:
            mycursor.execute("CREATE TABLE IF NOT EXISTS Borrow (BorrowID INT AUTO_INCREMENT PRIMARY KEY, UserID INT NOT NULL, BookID INT NOT NULL, BorrowDate DATE DEFAULT (CURRENT_DATE), ReturnDate DATE, FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE, FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE)")

        # Admin-Benutzer erstellen
        mycursor.execute(
            "INSERT INTO User (FirstName, LastName, Email, Permission, Passwort) VALUES (%s, %s, %s, %s, %s)",
            ('Admin', 'User', 'admin@email.com', 'Admin', 'admin')
        )

        # Änderungen speichern
        conn.commit()
        print("Admin user created successfully.")

    except mysql.connector.Error as err:
        tkinter.messagebox.showerror(title="Error", message=f"Failed to create tables or insert data: {err}")
        print(f"Error: {err}")
