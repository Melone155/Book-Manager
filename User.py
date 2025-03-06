import tkinter as tk
from tkinter import Frame, Label, Button, Entry


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

    canvas = tk.Canvas(root, width=900, height=50, bg="#FFFFFF")
    canvas.grid(row=0, column=0, columnspan=2, sticky='ew')

    search_entry = Entry(root, font=("Helvetica", 14))
    search_entry.grid(row=1, column=0, padx=7, pady=10)

    search_button = Button(root, text="Search", font=("Helvetica", 14),
                           command=lambda: search_users(root, conn, search_entry.get()))
    search_button.grid(row=1, column=1)

    container = Frame(root, bg="white")
    container.grid(row=2, column=0, columnspan=2, padx=3, pady=3, sticky='nsew')

    main_frame = Frame(container)
    main_frame.pack(padx=0, pady=0, expand=True, fill='both')

    if not users:
        no_data_label = Label(main_frame, text="No users found.", font=("Helvetica", 16))
        no_data_label.pack(padx=0, pady=0)
    else:
        row = 0
        for user in users:
            frame = Frame(main_frame, borderwidth=1, relief="solid", pady=5, padx=5, bg="white")
            frame.grid(row=row, column=0, padx=0, pady=0, sticky='ew')

            name_label = Label(frame, text=f"{user['FirstName']} {user['LastName']}", font=("Helvetica", 16))
            name_label.pack(side="left", padx=5, pady=5)

            details_button = Button(frame, text=">", font=("Helvetica", 16),
                                    command=lambda u=user: show_user_details(root, u))
            details_button.pack(side="right", padx=5, pady=5)

            row += 1

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)


def show_user_details(root, user):
    print(f"Show details for {user['FirstName']} {user['LastName']}")
