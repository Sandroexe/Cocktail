import requests
import tkinter as tk
from tkinter import ttk

# Hauptfenster erstellen
root = tk.Tk()
root.title("Suchfenster")
root.geometry("300x150")  # Fenstergröße

# Label und Eingabefeld für Name
name_label = ttk.Label(root, text="Name:")
name_label.pack(pady=(10, 0))
name_entry = ttk.Entry(root, width=30)
name_entry.pack(pady=5)

# Label und Eingabefeld für Zutat
ingredient_label = ttk.Label(root, text="Zutat:")
ingredient_label.pack(pady=(10, 0))
ingredient_entry = ttk.Entry(root, width=30)
ingredient_entry.pack(pady=5)

# Suchbutton (funktioniert noch nicht)
search_button = ttk.Button(root, text="Suchen")
search_button.pack(pady=10)

# Fenster starten
root.mainloop()

