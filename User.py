import tkinter as tk
from tkinter import Frame, Label, Button, Entry

import BookDetails
import MySQL


def search_users(root, conn, query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT UserID, FirstName, LastName, Permission FROM User WHERE FirstName LIKE %s OR LastName LIKE %s OR Permission LIKE %s",
        ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    users = cursor.fetchall()
    cursor.close()
    display_users(root, users, conn)


def display_users(root, conn):

    for widget in root.winfo_children():
        widget.destroy()

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT UserID, FirstName, LastName, Permission FROM User")
    users = cursor.fetchall()
    cursor.close()

    canvas = tk.Canvas(root, width=900, height=50, bg="white")
    canvas.grid(row=0, column=0, columnspan=2, sticky='ew')

    back = tk.Label(root, text="Back", font=("Helvetica", 16), bg="white", height=1, fg="black")
    back.place(x=20, y=10)
    back.bind("<Button-1>", lambda event: BookDetails.display_books(root, conn))

    search_entry = Entry(root, font=("Helvetica", 14))
    search_entry.grid(row=1, column=0, padx=7, pady=10)

    search_button = Button(root, text="Search", font=("Helvetica", 14), command=lambda: search_users(root, conn, search_entry.get()))
    search_button.grid(row=1, column=1)

    container = Frame(root, bg="white")
    container.grid(row=2, column=0, columnspan=2, padx=3, pady=3, sticky='nsew')

    main_frame = Frame(container, bg="white")
    main_frame.pack(padx=0, pady=0, expand=True, fill='both')

    if not users:
        no_data_label = Label(main_frame, text="No users found.", font=("Helvetica", 16), bg="white", fg="black")
        no_data_label.pack(padx=0, pady=0)
    else:
        row = 0
        for user in users:
            frame = Frame(main_frame, borderwidth=1, relief="solid", pady=5, padx=5, bg="white")
            frame.grid(row=row, column=0, padx=0, pady=0, sticky='ew')

            name_label = Label(frame, text=f"{user['FirstName']} {user['LastName']}", font=("Helvetica", 16), bg="white", fg="black")
            name_label.pack(side="left", padx=5, pady=5)

            details_button = Button(frame, text=">", font=("Helvetica", 16), command=lambda user_id=user['UserID']: display_user_overview(root, conn, user_id))
            details_button.pack(side="right", padx=5, pady=5)

            row += 1

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)


def display_user_overview(root, conn, user_id):

    for widget in root.winfo_children():
        widget.destroy()

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT User.UserID, User.FirstName, User.LastName, User.Email, COALESCE(GROUP_CONCAT(Books.Title SEPARATOR ', '), 'No books borrowed') AS BorrowedBooks FROM User LEFT JOIN borrow ON User.UserID = borrow.UserID LEFT JOIN Books ON borrow.ISBN = Books.ISBN WHERE User.UserID = %s GROUP BY User.UserID", (user_id,))

    user = cursor.fetchone()
    cursor.close()

    header_frame = Frame(root, bg="white")
    header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

    Delete = tk.Label(root, text="Delet User", font=("Helvetica", 16), bg="white", fg="red")
    Delete.grid(row=0, column=1, sticky='e', padx=20)
    Delete.bind("<Button-1>", lambda event: MySQL.delete_user(root, conn, user['UserID']))

    back = tk.Label(header_frame, text="Back", font=("Helvetica", 16), bg="white", fg="black", cursor="hand2")
    back.grid(row=0, column=0, sticky='w', padx=10, pady=10)
    back.bind("<Button-1>", lambda event: BookDetails.display_books(root, conn))

    title_label = Label(header_frame, text="User Overview", font=("Helvetica", 18, "bold"), bg="white", fg="black")
    title_label.grid(row=0, column=1, columnspan=1, pady=10, sticky="n")
    header_frame.grid_columnconfigure(1, weight=2)

    container = Frame(root, bg="white")
    container.grid(row=1, column=0, columnspan=3, padx=3, pady=3, sticky='nsew')

    main_frame = Frame(container, bg="white")
    main_frame.pack(padx=0, pady=0, expand=True, fill='both')

    if not user:
        no_data_label = Label(container, text="User not found.", font=("Helvetica", 16), bg="white", fg="black")
        no_data_label.pack(pady=10)
    else:

        info_text = f"""
            Last Name: {user['LastName']}
            First Name: {user['FirstName']}
            Email: {user['Email']}
            User ID: {user['UserID']}
            """
        info_label = Label(container, text=info_text, font=("Helvetica", 14), bg="white", justify="left")
        info_label.pack(pady=10, anchor="w")

        borrowed_books = user.get('BorrowedBooks', "No books borrowed")
        books_label = Label(container, text=f"Borrowed Books: {borrowed_books}", font=("Helvetica", 12), fg="gray", bg="white", justify="left")
        books_label.pack(pady=5, anchor="w")