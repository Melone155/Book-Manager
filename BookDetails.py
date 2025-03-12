import tkinter as tk
from datetime import datetime, timedelta
from tkinter import Frame, Label, Entry, Button, messagebox

import AddBook
import MySQL
import User


def search_books(root, conn, query):
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Books.ISBN, Books.Title, Authors.Name FROM Books JOIN Authors ON Books.AuthorID = Authors.AuthorID WHERE Books.Title LIKE %s OR Authors.Name LIKE %s OR Books.ISBN LIKE %s", ('%' + query + '%',) * 4)

    books = cursor.fetchall()
    cursor.close()
    display_books(root, books, conn)


def display_books(root, conn):

    for widget in root.winfo_children():
        widget.destroy()

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Books.ISBN, Books.Title, Authors.Name FROM Books JOIN Authors ON Books.AuthorID = Authors.AuthorID")
    books = cursor.fetchall()
    cursor.close()

    canvas = tk.Canvas(root, width=900, height=50, bg="#FFFFFF")
    canvas.grid(row=0, column=0, columnspan=2, sticky='ew')

    if MySQL.permissions == "Admin":
        add = tk.Label(root, text="Add Book", font=("Helvetica", 16), bg="white", fg="black")
        add.grid(row=0, column=1, sticky='e', padx=20)
        add.bind("<Button-1>", lambda event: AddBook.add_book(root, conn))

        user = tk.Label(root, text="User", font=("Helvetica", 16), bg="white", fg="black")
        user.grid(row=0, column=0, sticky='w', padx=20)
        user.bind("<Button-1>", lambda event: User.display_users(root, MySQL.conn))
    else:
        canvas.create_text(450, 25, text="Book-Manager", font=("Helvetica", 16))

    searchentry = tk.Entry(root, fg="black")
    searchentry.grid(row=1, column=0, padx=7, pady=10)

    search_button = Button(root, text="Search", font=("Helvetica", 14),bg="white", command=lambda: search_books(root, conn, searchentry.get()))
    search_button.grid(row=1, column=1)


    container = Frame(root, bg="white")
    container.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

    main_frame = Frame(container, bg="white")
    main_frame.pack(padx=5, pady=5, expand=True, fill='both')

    if not books:
        no_data_label = Label(main_frame, text="No books found.", font=("Helvetica", 16), bg="white", fg="black")
        no_data_label.pack(padx=5, pady=5)
    else:
        row = 0
        for book in books:
            frame = Frame(main_frame, borderwidth=1, relief="solid", pady=5, padx=5, bg="white")
            frame.grid(row=row, column=0, padx=0, pady=0, sticky='ew')

            title_label = Label(frame, text=book['Title'], font=("Helvetica", 16), bg="white", fg="black")
            title_label.pack(side="left", padx=5, pady=5)

            details_button = Button(frame, text=">", font=("Helvetica", 16),command=lambda: book_details(root, conn, book['ISBN']), fg="black")
            details_button.pack(side="right", padx=5, pady=5)

            row += 1

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)


import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta


def book_details(root, conn, book_id, user_id):
    # Vorherigen Inhalt löschen
    for widget in root.winfo_children():
        widget.destroy()

    cursor = conn.cursor(dictionary=True)

    # Buch-Details abrufen (inkl. Ausleihstatus)
    cursor.execute("""
        SELECT Books.Title, Authors.Name AS Author, Books.ReleaseDate, Borrow.ReturnDate
        FROM Books 
        JOIN Authors ON Books.AuthorID = Authors.AuthorID
        LEFT JOIN Borrow ON Books.ISBN = Borrow.ISBN AND Borrow.ReturnDate IS NULL
        WHERE Books.ISBN = %s
    """, (book_id,))

    book = cursor.fetchone()
    cursor.close()

    if not book:
        messagebox.showerror("Fehler", "Buch nicht gefunden.")
        return

    title = book["Title"]
    author = book["Author"]
    release_date = book["ReleaseDate"]
    return_date = book["ReturnDate"]

    # UI erstellen
    root.configure(bg="white")

    # Zurück-Button
    back_button = tk.Button(root, text="Zurück", font=("Helvetica", 14),
                            command=lambda: display_books(root, conn, user_id))
    back_button.place(x=20, y=20)

    # Buchinformationen
    tk.Label(root, text=title, font=("Helvetica", 20, "bold"), bg="white").pack(pady=20)
    tk.Label(root, text=f"Autor: {author}", font=("Helvetica", 16), bg="white").pack(pady=5)
    tk.Label(root, text=f"Erscheinungsdatum: {release_date}", font=("Helvetica", 16), bg="white").pack(pady=5)

    # Ausleihen-Button
    loan_button = tk.Button(root, text="Buch ausleihen", font=("Helvetica", 16),
                            command=lambda: borrow_book(root, conn, book_id, user_id))
    loan_button.pack(side="bottom", padx=20, pady=20, anchor="se")

    if return_date:
        return_date_formatted = datetime.strptime(str(return_date), "%Y-%m-%d").strftime('%d.%m.%Y')
        tk.Label(root, text=f"Bereits ausgeliehen! Rückgabe am: {return_date_formatted}", font=("Helvetica", 14),
                 fg="red", bg="white").pack(pady=10)
        loan_button.config(state="disabled")


def borrow_book(root, conn, book_id, user_id):
    cursor = conn.cursor()

    # Prüfen, ob das Buch bereits ausgeliehen wurde (noch nicht zurückgegeben)
    cursor.execute("SELECT ReturnDate FROM Borrow WHERE ISBN = %s AND ReturnDate IS NULL", (book_id,))
    loan = cursor.fetchone()

    if loan:
        messagebox.showwarning("Nicht möglich", "Das Buch ist bereits ausgeliehen.")
    else:
        return_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
        cursor.execute("INSERT INTO Borrow (UserID, ISBN, ReturnDate) VALUES (%s, %s, %s)",
                       (user_id, book_id, return_date))
        conn.commit()
        messagebox.showinfo("Erfolgreich", "Das Buch wurde ausgeliehen!")
        book_details(root, conn, book_id, user_id)  # Ansicht aktualisieren

    cursor.close()