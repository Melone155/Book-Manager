import tkinter as tk
from tkinter import Entry, Button

import MySQL


def get_books_from_db(conn):

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ISBN, title, AuthorID FROM Books")
    books = cursor.fetchall()
    cursor.close()
    return books


def search_books(root, conn, query):
    cursor = conn.cursor(dictionary=True)

    # Erweiterte SQL-Abfrage für ISBN
    cursor.execute("SELECT Books.ISBN, Books.Title, Authors.FirstName, Authors.LastName FROM Books JOIN Authors ON Books.AuthorID = Authors.AuthorID WHERE Books.Title LIKE %s OR Authors.FirstName LIKE %s OR Authors.LastName LIKE %s  OR Books.ISBN LIKE %s" , ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))

    books = cursor.fetchall()
    cursor.close()
    display_books(root, books, conn)

def display_books(root, books, conn):
    for widget in root.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(root, width=900, height=50, bg="#FFFFFF")
    canvas.grid(row=0, column=0, columnspan=2, sticky='ew')

    if MySQL.permissions == "Admin":
        add = tk.Label(root, text="Add Book", font=("Helvetica", 16), bg="white")
        add.grid(row=0, column=1, sticky='e', padx=20)
        add.bind("<Button-1>") #lambda event: AddEmployee.AddEmployee(root)

        user = tk.Label(root, text="User", font=("Helvetica", 16), bg="white")
        user.grid(row=0, column=0, sticky='w', padx=20)
        user.bind("<Button-1>")
    else:
        canvas.create_text(450, 25, text="Book-Manager", font=("Helvetica", 16))

    search_entry = Entry(root, font=("Helvetica", 14))
    search_entry.grid(row=1, column=0, padx=7, pady=10)

    search_button = Button(root, text="Search", font=("Helvetica", 14),
                           command=lambda: search_books(root, conn, search_entry.get()))
    search_button.grid(row=1, column=1)

    row = 2
    for book in books:
        label = tk.Label(root, text=f"{book['Title']}", font=("Helvetica", 14))
        label.grid(row=row, column=0, sticky="w", padx=10)

        # Anzeige des Autoren-Namens
        author_name = f"{book['FirstName']} {book['LastName']}"
        author_label = tk.Label(root, text=f"by {author_name}", font=("Helvetica", 12), fg="gray")
        author_label.grid(row=row, column=1, sticky="w")

        # Anzeige der ISBN (als BookID)
        isbn_label = tk.Label(root, text=f"ISBN: {book['ISBN']}", font=("Helvetica", 12), fg="gray")
        isbn_label.grid(row=row, column=2, sticky="w")

        row += 1

