import tkinter as tk
from tkinter import ttk

import customtkinter
from customtkinter.windows.widgets import ctk_button

import BookDetails


def add_book(root, conn):

    for widget in root.winfo_children():
        widget.destroy()

    # Verbindung global speichern
    global isbnentry, titleentry, yearentry, authorchoice, author_dropdown, author_entry_name, conn_global
    conn_global = conn

    back = tk.Label(root, text="Back", font=("Helvetica", 14), bg="white", fg="black")
    back.grid(row=0, column=0, sticky="w", padx=20)
    back.bind("<Button-1>", lambda event: BookDetails.display_books(root, conn))

    isnlabel = tk.Label(root, text="ISBN:", font=("Helvetica", 16), bg="white", fg="black")
    isnlabel.place(x=336, y=100)
    isbnentry = tk.Entry(root)
    isbnentry.place(x=410, y=107)

    titlelabel = tk.Label(root, text="Title:", font=("Helvetica", 16), bg="white", fg="black")
    titlelabel.place(x=336, y=135)
    titleentry = tk.Entry(root)
    titleentry.place(x=410, y=142)

    yearlabel = tk.Label(root, text="Year of publication:", font=("Helvetica", 16), bg="white", fg="black")
    yearlabel.place(x=210, y=170)
    yearentry = tk.Entry(root)
    yearentry.place(x=410, y=177)

    authorchoice = tk.StringVar(value="existing")

    frame = tk.Frame(root, bg="white")
    frame.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    tk.Radiobutton(root, text="Existing Author", variable=authorchoice, value="existing", bg="white", command=update_author_selection, fg="black").place(x=350, y=220)

    tk.Radiobutton(root, text="New Author", variable=authorchoice, value="new", bg="white", command=update_author_selection, fg="black").place(x=480, y=220)

    author_dropdown = ttk.Combobox(root, width=27, state="normal")
    author_dropdown.place(x=370, y=250)

    author_entry_name = tk.Entry(root, width=30, state="disabled")
    author_entry_name.place(x=370, y=280)

    load_existing_authors()

    main_font = customtkinter.CTkFont(family="Helvetica", size=12)

    Save_Button = ctk_button.CTkButton(
        master=root,
        text="Save",
        font=main_font,
        text_color="black",
        height=40,
        width=120,
        border_width=2,
        corner_radius=3,
        border_color="#d3d3d3",
        bg_color="#ffffff",
        fg_color="#ffffff",
        hover=False,
        command=lambda: save_book()
    )

    Save_Button.place(x=400, y=310)

def update_author_selection():

    if authorchoice.get() == "existing":
        author_dropdown.config(state="normal")
        author_entry_name.config(state="disabled")
    else:
        author_dropdown.config(state="disabled")
        author_entry_name.config(state="normal")

def load_existing_authors():

    cursor = conn_global.cursor()
    cursor.execute("SELECT Name FROM Authors ORDER BY Name ASC")
    authors = [row[0] for row in cursor.fetchall()]
    cursor.close()
    author_dropdown["values"] = authors

def save_book():

    isbn = isbnentry.get()
    title = titleentry.get()
    year = yearentry.get()
    author_name = author_entry_name.get() if authorchoice.get() == "new" else author_dropdown.get()

    if not isbn or not title or not year or not author_name:
        tk.messagebox.showerror(title="Error", message="Please fill in all fields!")
        return

    cursor = conn_global.cursor()

    try:

        if authorchoice.get() == "new":
            cursor.execute("INSERT INTO Authors (Name) VALUES (%s)", (author_name,))
            conn_global.commit()

        # Autor-ID abrufen
        cursor.execute("SELECT AuthorID FROM Authors WHERE Name = %s", (author_name,))
        author_id = cursor.fetchone()

        if not author_id:
            tk.messagebox.showerror(title="Error", message="Author not found")
            cursor.close()
            return

        cursor.execute("INSERT INTO Books (ISBN, Title, PublicationYear, AuthorID) VALUES (%s, %s, %s, %s)", (isbn, title, year, author_id[0]))
        conn_global.commit()

        tk.messagebox.showinfo(title="Book Add", message="Book added successfully!")
        cursor.close()

    except Exception as e:
        conn_global.rollback()
        tk.messagebox.showerror(title="Error", message=f"Failed to add book: {e}")
        cursor.close()
