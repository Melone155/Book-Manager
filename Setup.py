import tkinter as tk

from PIL import Image, ImageTk
import customtkinter
import customtkinter as ctk
import os

import Login
import MySQL

def Setupstart(root):
    MySQL = 'Config/MySQL.yaml'

    global var
    var = tk.StringVar()

    if not os.path.exists(MySQL):

        image = Image.open("Picture/Logo.png").convert("RGBA")
        background = Image.new("RGBA", image.size, (255, 255, 255, 255))  # Weißer Hintergrund
        background.paste(image, (0, 0), image)
        tk_image = ImageTk.PhotoImage(background)

        label = tk.Label(root, image=tk_image)
        label.image = tk_image
        label.pack(pady=20)

        main_font = customtkinter.CTkFont(family="Helvetica", size=12)

        Setup_Wizard_Button = ctk.CTkButton(
            master=root,
            text="Setup Wizard",
            command=lambda: (SetupMySQL(root)),
            font=main_font,
            text_color="black",
            height=40,
            width=120,
            border_width=2,
            corner_radius=3,
            border_color="#d3d3d3",
            bg_color="#ffffff",
            fg_color="#ffffff",
            hover=False
        )

        Setup_Wizard_Button.place(x=400, y=400)
    else:
        #Login.LoginScreen(root)
        print("Setup Finish")

def SetupMySQL(root):
    # Clear All Old Objects
    for widget in root.winfo_children():
        widget.destroy()

    # Logo laden
    image = Image.open("Picture/Logo.png").convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))  # Weißer Hintergrund
    background.paste(image, (0, 0), image)
    tk_image = ImageTk.PhotoImage(background)

    label = ctk.CTkLabel(root, image=tk_image, text="")
    label.image = tk_image
    label.pack(pady=20)

    main_font = ctk.CTkFont(family="Helvetica", size=12)

    #Host
    hostlabe = tk.Label(root, bg="white", text="MySQL Host:", font=("Helvetica", 16))
    hostlabe.place(x=120, y=300)

    hostentry = tk.Entry(root)
    hostentry.place(x=260, y=305)
    hostentry.insert(0, "localhost")

    #Port
    portlabe = tk.Label(root, bg="white", text="Port:", font=("Helvetica", 16))
    portlabe.place(x=200, y=340)

    portentry = tk.Entry(root)
    portentry.place(x=260, y=345)
    portentry.insert(0, "3306")

    #User
    userlabe = tk.Label(root, bg="white", text="User:", font=("Helvetica", 16))
    userlabe.place(x=195, y=380)

    userentry = tk.Entry(root)
    userentry.place(x=260, y=385)
    userentry.insert(0, "root")

    #Database
    databaselabe = tk.Label(root, bg="white", text="Database:", font=("Helvetica", 16))
    databaselabe.place(x=150, y=420)

    databaseentry = tk.Entry(root)
    databaseentry.place(x=260, y=425)
    databaseentry.insert(0, "bookmanager")

    #Passwort
    passwordlabe = tk.Label(root, bg="white", text="Password:", font=("Helvetica", 16))
    passwordlabe.place(x=150, y=460)

    passwordentry = tk.Entry(root, show="*")
    passwordentry.place(x=260, y=465)

    # Test-Button
    test_button = ctk.CTkButton(
        master=root,
        text="Test Connection",
        font=main_font,
        command=lambda: MySQL.test_mysql_connection(
            hostentry.get(),
            portentry.get(),
            userentry.get(),
            passwordentry.get(),
            databaseentry.get()
        )
    )
    test_button.place(x=600, y=547)

    # Next-Button
    next_button = ctk.CTkButton(
        master=root,
        text="Next",
        command=lambda: Finishsetup(root),
        font=main_font,
        text_color="black",
        height=40,
        width=120,
        border_width=2,
        corner_radius=3,
        border_color="#d3d3d3",
        bg_color="#ffffff",
        fg_color="#ffffff",
        hover=False
    )
    next_button.place(x=750, y=540)

def Finishsetup(root):
    MySQL = 'Config/MySQL.yaml'
    if not os.path.exists(MySQL):
        tk.messagebox.showerror(title="Error", message="Please test the connection")
    else:
        for widget in root.winfo_children():
            widget.destroy()
    Login.LoginScreen(root)