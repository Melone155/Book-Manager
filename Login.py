import tkinter as tk
from PIL import Image, ImageTk
import customtkinter
from customtkinter.windows.widgets import ctk_button
import MySQL
import Register


def LoginScreen(root):

    # Clear All Old Objects
    for widget in root.winfo_children():
        widget.destroy()

    image = Image.open("Picture/Logo.png").convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))  # Weißer Hintergrund
    background.paste(image, (0, 0), image)
    tk_image = ImageTk.PhotoImage(background)

    label = tk.Label(root, image=tk_image)
    label.image = tk_image
    label.pack(pady=20)

    Emaillabe = tk.Label(root, bg="white", text="Email", font=("Helvetica", 16), fg="black")
    Emaillabe.place(x=336, y=284)

    Emailentry = tk.Entry(root)
    Emailentry.place(x=440, y=290)

    passwordlabe = tk.Label(root, bg="white", text="Password", font=("Helvetica", 16), fg="black")
    passwordlabe.place(x=336, y=319)

    passwordentry = tk.Entry(root, show="*")
    passwordentry.place(x=440, y=325)

    main_font = customtkinter.CTkFont(family="Helvetica", size=12)

    Login_Button = ctk_button.CTkButton(
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
        command=lambda: MySQL.Login(MySQL.conn, Emailentry.get(), passwordentry.get(), root)
                                    #conn, email, password, root
    )

    Login_Button.place(x=387, y=360)

    Regist_Button = ctk_button.CTkButton(
        master=root,
        text="Register",
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
        command=lambda: Register.RegisterScreen(root)
    )

    Regist_Button.place(x=387, y=410)