import tkinter as tk
from PIL import Image, ImageTk
import customtkinter
import customtkinter as ctk

import Login
import MySQL


def RegisterScreen(root):
    # Clear All Old Objects
    for widget in root.winfo_children():
        widget.destroy()

    # Logo laden
    image = Image.open("Picture/Logo.png").convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))  # Weißer Hintergrund
    background.paste(image, (0, 0), image)
    tk_image = ImageTk.PhotoImage(background)

    label = tk.Label(root, image=tk_image)
    label.image = tk_image
    label.pack(pady=20)

    main_font = ctk.CTkFont(family="Helvetica", size=12)

    #FirstName
    Fistnamelabe = tk.Label(root, bg="white", text="First Name:", font=("Helvetica", 16), fg="black")
    Fistnamelabe.place(x=120, y=300)
    Firnameentry = tk.Entry(root)
    Firnameentry.place(x=260, y=305)

    #LastName
    Lastnamelabe = tk.Label(root, bg="white", text="Last Name:", font=("Helvetica", 16), fg="black")
    Lastnamelabe.place(x=120, y=340)
    Lastnameentry = tk.Entry(root)
    Lastnameentry.place(x=260, y=345)

    #Email
    Emaillabe = tk.Label(root, bg="white", text="Email:", font=("Helvetica", 16), fg="black")
    Emaillabe.place(x=120, y=380)
    Emailentry = tk.Entry(root)
    Emailentry.place(x=260, y=385)

    #Passwort
    passwordlabe = tk.Label(root, bg="white", text="Password:", font=("Helvetica", 16), fg="black")
    passwordlabe.place(x=120, y=420)
    passwordentry = tk.Entry(root, show="*")
    passwordentry.place(x=260, y=425)

    # Next-Button
    register_button = ctk.CTkButton(
        master=root,
        text="Register",
        command=lambda: (MySQL.RegisterMySQL(MySQL.conn, Emailentry.get(), Firnameentry.get(), Lastnameentry.get(), passwordentry.get()), Login.LoginScreen(root)),
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
    register_button.place(x=750, y=540)

    back_button = ctk.CTkButton(
        master=root,
        text="Back",
        command=lambda: Login.LoginScreen(root),
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
    back_button.place(x=50, y=540)