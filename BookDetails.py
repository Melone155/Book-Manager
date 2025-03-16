import tkinter as tk
from tkinter import Frame, Label, Button, messagebox

import AddBook
import MySQL
import User


def search_books(root, conn, query):
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Books.ISBN, Books.Title, Authors.Name FROM Books JOIN Authors ON Books.AuthorID = Authors.AuthorID  WHERE Books.Title LIKE %s OR Authors.Name LIKE %s OR Books.ISBN LIKE %s", (query + '%', '%' + query + '%', '%' + query + '%'))

    books = cursor.fetchall()
    cursor.close()
    display_books(root, conn, books)


def display_books(root, conn, books=None):
    for widget in root.winfo_children():
        widget.destroy()

    if books is None:
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

    search_button = Button(root, text="Search", font=("Helvetica", 14), bg="white",
                           command=lambda: search_books(root, conn, searchentry.get()))
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

            details_button = Button(frame, text=">", font=("Helvetica", 16), command=lambda book_id=book['ISBN']: book_details(root, conn, book_id, MySQL.UserID), fg="black")
            details_button.pack(side="right", padx=5, pady=5)

            row += 1

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)


def book_details(root, conn, book_id, user_id):

    for widget in root.winfo_children():
        widget.destroy()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Books.Title, Authors.Name AS Author, Books.PublicationYear, Borrow.UserID AS BorrowedBy FROM Books JOIN Authors ON Books.AuthorID = Authors.AuthorID JOIN Borrow ON Books.ISBN = Borrow.ISBN WHERE Books.ISBN = %s", (book_id,))

    book = cursor.fetchone()
    cursor.close()

    if not book:
        messagebox.showerror("Error", "The book you selected could not be found.")
        return

    title = book["Title"]
    author = book["Author"]
    release_date = book["PublicationYear"]
    borrowed_by = book["BorrowedBy"]

    back_button = tk.Button(root, text="Back", font=("Helvetica", 14), command=lambda: display_books(root, conn))
    back_button.place(x=20, y=20)

    tk.Label(root, text=title, font=("Helvetica", 20, "bold"), bg="white").pack(pady=20)
    tk.Label(root, text=f"Autor: {author}", font=("Helvetica", 16), bg="white").pack(pady=5)
    tk.Label(root, text=f"Publication date: {release_date}", font=("Helvetica", 16), bg="white").pack(pady=5)

    button_frame = tk.Frame(root, bg="white")
    button_frame.pack(pady=20)

    if borrowed_by:
        tk.Label(root, text="The book is currently out on loan!", font=("Helvetica", 14), fg="red", bg="white").pack(
            pady=10)

        if borrowed_by == user_id:
            return_button = tk.Button(button_frame, text="Return book", font=("Helvetica", 16),
                                      command=lambda: return_book(root, conn, book_id, user_id))
            return_button.pack(side="left", padx=10)
        else:
            loan_button = tk.Button(button_frame, text="Borrow a book", font=("Helvetica", 16), state="disabled")
            loan_button.pack(side="left", padx=10)


def borrow_book(root, conn, book_id, user_id):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Borrow WHERE ISBN = %s", (book_id,))
    existing_borrow = cursor.fetchone()

    if existing_borrow:
        messagebox.showerror("Error", "The book is already on loan.")
    else:

        cursor.execute("INSERT INTO Borrow (UserID, ISBN) VALUES (%s, %s)", (user_id, book_id))
        conn.commit()
        messagebox.showinfo("Successful", "Book successfully borrowed!")

    cursor.close()
    book_details(root, conn, book_id, user_id)

    cursor.close()


def return_book(root, conn, book_id, user_id):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Borrow WHERE ISBN = %s AND UserID = %s", (book_id, user_id))
    conn.commit()
    cursor.close()

    messagebox.showinfo("Successful", "The book has been returned!")
    book_details(root, conn, book_id, user_id)
