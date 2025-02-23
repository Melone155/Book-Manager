import tkinter as tk

import Setup

# Hauptfenster erstellen
root = tk.Tk()
root.title("Book Management")
root.geometry("900x600")
root.configure(bg='white')

# Setup Wizard starten
Setup.Setupstart(root)

# GUI-Schleife starten
root.mainloop()