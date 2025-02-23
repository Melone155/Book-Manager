import tkinter as tk

from PIL import Image, ImageTk
import  customtkinter
import customtkinter as ctk
import os

import MySQL
def LoginScreen(root):
    # Clear All Old Objects
    for widget in root.winfo_children():
        widget.destroy()

    image = Image.open("Picture/Logo.png")
    image = image.resize((306, 218))  # Größe anpassen
    tk_image = ImageTk.PhotoImage(image)

    label = tk.Label(root, image=tk_image)
    label.image = tk_image
    label.pack(pady=20)

    Userlabe = tk.Label(root, text="Username", font=("Helvetica", 16))
    Userlabe.place(x=336, y=284)

    Userentry = tk.Entry(root)
    Userentry.place(x=440, y=290)

    passwordlabe = tk.Label(root, text="Password", font=("Helvetica", 16))
    passwordlabe.place(x=336, y=319)

    passwordentry = tk.Entry(root, show="*")
    passwordentry.place(x=440, y=325)

    main_font = customtkinter.CTkFont(family="Helvetica", size=12)

    Setup_Wizard_Button = ctk_button.CTkButton(
        master=root,
        text="Login",
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
        command=lambda: Login(Userentry.get(), passwordentry.get(), root)
    )

    Setup_Wizard_Button.place(x=387, y=360)