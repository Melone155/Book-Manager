import tkinter as tk
from tkinter import Frame, Label, Entry, Button

import MySQL
import User


def search_books(root, conn, query):
    """Sucht Bücher nach Titel, Autor oder ISBN und zeigt die Ergebnisse an."""
    cursor = conn.cursor(dictionary=True)

    # Erweiterte SQL-Abfrage für die Suche
    cursor.execute("""
        SELECT Books.ISBN, Books.Title, Authors.FirstName, Authors.LastName 
        FROM Books 
        JOIN Authors ON Books.AuthorID = Authors.AuthorID 
        WHERE Books.Title LIKE %s 
        OR Authors.FirstName LIKE %s 
        OR Authors.LastName LIKE %s  
        OR Books.ISBN LIKE %s
    """, ('%' + query + '%',) * 4)

    books = cursor.fetchall()
    cursor.close()
    display_books(root, books, conn)


def display_books(root, conn):
    """Zeigt eine Liste von Büchern in einer Art DataGrid mit weißen Hintergründen an."""

    # Vorherige Inhalte löschen, um die Ansicht zu aktualisieren
    for widget in root.winfo_children():
        widget.destroy()

    # Bücher aus der Datenbank abrufen
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Books.ISBN, Books.Title, Authors.FirstName, Authors.LastName 
        FROM Books 
        JOIN Authors ON Books.AuthorID = Authors.AuthorID
    """)
    books = cursor.fetchall()
    cursor.close()

    # Oberes Menü
    canvas = tk.Canvas(root, width=900, height=50, bg="#FFFFFF")
    canvas.grid(row=0, column=0, columnspan=2, sticky='ew')

    if MySQL.permissions == "Admin":
        add = tk.Label(root, text="Add Book", font=("Helvetica", 16), bg="white")
        add.grid(row=0, column=1, sticky='e', padx=20)
        add.bind("<Button-1>")  # Hier kannst du später die Funktion zum Hinzufügen implementieren

        user = tk.Label(root, text="User", font=("Helvetica", 16), bg="white")
        user.grid(row=0, column=0, sticky='w', padx=20)
        user.bind("<Button-1>", lambda event: User.display_users(root, MySQL.conn))
    else:
        canvas.create_text(450, 25, text="Book-Manager", font=("Helvetica", 16))

    # Suchleiste
    search_entry = Entry(root, font=("Helvetica", 14))
    search_entry.grid(row=1, column=0, padx=7, pady=10)

    search_button = Button(root, text="Search", font=("Helvetica", 14),
                           command=lambda: search_books(root, conn, search_entry.get()))
    search_button.grid(row=1, column=1)

    # Container für die Bücherliste (mit weißem Hintergrund)
    container = Frame(root, bg="white")  # Hintergrund auf weiß setzen
    container.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

    main_frame = Frame(container, bg="white")  # Hintergrund auf weiß setzen
    main_frame.pack(padx=5, pady=5, expand=True, fill='both')

    if not books:
        no_data_label = Label(main_frame, text="No books found.", font=("Helvetica", 16), bg="white")
        no_data_label.pack(padx=5, pady=5)
    else:
        row = 0
        for book in books:
            frame = Frame(main_frame, borderwidth=1, relief="solid", padx=10, pady=5, bg="white")
            frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

            # Buchtitel
            title_label = Label(frame, text=book['Title'], font=("Helvetica", 14), bg="white")
            title_label.pack(side="top", anchor="w")

            # Autor & ISBN
            author_label = Label(frame, text=f"by {book['FirstName']} {book['LastName']} | ISBN: {book['ISBN']}",
                                 font=("Helvetica", 12), fg="gray", bg="white")
            author_label.pack(side="top", anchor="w")

            # Button für Details
            view_button = Button(frame, text=">", font=("Helvetica", 14),
                                 command=lambda isbn=book['ISBN']: show_book_details(root, isbn))
            view_button.pack(side="right", padx=5, pady=5)

            row += 1

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)


def show_book_details(root, isbn):
    """Öffnet eine Detailansicht für das gewählte Buch."""
    print(f"Details für Buch mit ISBN {isbn} anzeigen")
