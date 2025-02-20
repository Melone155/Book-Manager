import tkinter as tk

from PIL import Image, ImageTk
import  customtkinter
import customtkinter as ctk
import os

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
            command=lambda: start_Wizard(root),
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

def start_Wizard(root):

    image = Image.open("Picture/Logo.jpg")
    image = image.resize((460, 327))
    tk_image = ImageTk.PhotoImage(image)

    #Clear All Old Objects
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, image=tk_image)
    label.image = tk_image
    label.pack(pady=20)

    headline = tk.Label(root, text="What are you MySQl Credentials", font=("Helvetica", 16))
    headline.place(x=300, y=375)

    namelabel = tk.Label(root, text="User Name", font=("Helvetica", 16))
    namelabel.place(x=50, y=100)

    main_font = customtkinter.CTkFont(family="Helvetica", size=12)

    Setup_Wizard_Button = ctk.CTkButton(
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

    Setup_Wizard_Button.place(x=397, y=480)

def Finishsetup(root):
        #YML.CreateConfigs()
        #Login.LoginScreen(root)
        print("")