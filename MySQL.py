import sys
from tkinter import messagebox
import mysql.connector

import User
import YML
import BookDetails

def test_mysql_connection(host, port, user, password, database):
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

        mycursor.execute("SHOW TABLES LIKE 'Author'")
        resultAuthor = mycursor.fetchone()

        if not resultAuthor:
            mycursor.execute("CREATE TABLE IF NOT EXISTS Authors (AuthorID INT AUTO_INCREMENT PRIMARY KEY, FirstName VARCHAR(50) NOT NULL, LastName VARCHAR(50) NOT NULL);")
        if not resultBook:
            mycursor.execute("CREATE TABLE IF NOT EXISTS Books (ISBN VARCHAR(255) PRIMARY KEY, Title VARCHAR(50) NOT NULL, PublicationYear YEAR NOT NULL, AuthorID INT, FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID) ON DELETE SET NULL);")
        if not resultUser:
            mycursor.execute("CREATE TABLE IF NOT EXISTS User (UserID INT AUTO_INCREMENT PRIMARY KEY, FirstName VARCHAR(100) NOT NULL, LastName VARCHAR(100) NOT NULL, Email VARCHAR(255) UNIQUE NOT NULL, Permission VARCHAR(5) NOT NULL, Passwort VARCHAR(255) NOT NULL)")
        if not resultBorrow:
            mycursor.execute("CREATE TABLE IF NOT EXISTS Borrow (BorrowID INT AUTO_INCREMENT PRIMARY KEY, UserID INT NOT NULL, ISBN VARCHAR(13) NOT NULL, BorrowDate DATE DEFAULT (CURRENT_DATE), ReturnDate DATE, FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE, FOREIGN KEY (ISBN) REFERENCES Books(ISBN) ON DELETE CASCADE);")

        mycursor.execute(
            "INSERT INTO User (FirstName, LastName, Email, Permission, Passwort) VALUES (%s, %s, %s, %s, %s)",
            ('Admin', 'User', 'admin@email.com', 'Admin', 'admin')
        )

        conn.commit()

    except mysql.connector.Error as err:
        tkinter.messagebox.showerror(title="Error", message=f"Failed to create tables or insert data: {err}")
        print(f"Error: {err}")


def ConnectionMySQL():
    config = YML.load_mysql_config()

    if config is None:
        return None

    try:
        conn = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )
        return conn
    except mysql.connector.Error as err:#
        tkinter.messagebox.showerror(title="Error", message=f"Connection failed: {err}")
        sys.exit()


conn = ConnectionMySQL()


import tkinter

def RegisterMySQL(conn, email, FirstName, LastName, Passwort):
    # Prüfen, ob die Verbindung existiert
    if conn is None:
        tkinter.messagebox.showerror(title="Error", message="Datenbankverbindung nicht vorhanden.")
        return

    mycursor = conn.cursor()

    mycursor.execute("SELECT COUNT(*) FROM User WHERE Email = %s", (email,))
    (count,) = mycursor.fetchone()

    if count == 0:
        mycursor.execute(
            "INSERT INTO User (FirstName, LastName, Email, Permission, Passwort) VALUES (%s, %s, %s, %s, %s)",
            (FirstName, LastName, email, 'User', Passwort)
        )
        conn.commit()
        tkinter.messagebox.showinfo(title="Create", message="Your account has been successfully created")
    else:
        tkinter.messagebox.showerror(title="Error", message="The e-mail address is already in use.")

    conn.close()

permissions = ""

def Login(conn, email, password, root):
    global permissions

    if not conn:
        tkinter.messagebox.showerror(title="Connection Error", message="No connection to the database could be established.")
        return

    mycursor = conn.cursor(dictionary=True)  #'dictionary=True' Makes sure that the return is structured as an array and all information is a string
    mycursor.execute("SELECT * FROM User WHERE Email = %s AND Passwort = %s", (email, password))
    user = mycursor.fetchone()

    if user:
        permissions = user['Permission']

        BookDetails.display_books(root, conn)
    else:
        tkinter.messagebox.showerror(title="Login Failed", message="Invalid email or password.")


def delete_user(root, conn, user_id):

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
    if not confirm:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))
        conn.commit()

        messagebox.showinfo("Success", "User deleted successfully!")
        User.display_users(root, conn)

        cursor.close()

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to delete user: {e}")
        cursor.close()


