import tkinter as tk
from tkinter import messagebox
import requests

# --- Funktionen ---
# Cocktail-Datenbank durchsuchen
def suche_cocktail():
    name = eingabe.get().strip()
    if not name:
        print("Error, Kein Name eingegeben")
        messagebox.showwarning("Hinweis", "Bitte gib einen Cocktailnamen ein.")
        return

    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"
    try:
        antwort = requests.get(url)
        daten = antwort.json()
    except Exception as e:
        print("Hinweis", f"API-Fehler:\n{e}")
        messagebox.showerror("Hinweis", f"API-Fehler:\n{e}")
        return

    liste.delete(0, tk.END)
    global ergebnisse, modus
    ergebnisse = daten.get("drinks")
    modus = "cocktail"

    if not ergebnisse:
        liste.insert(tk.END, "Keine Ergebnisse gefunden.")
        return

    for drink in ergebnisse:
        liste.insert(tk.END, drink["strDrink"])


# Zutaten-Datenbank durchsuchen (zeigt alle Cocktails, die diese Zutat enthalten)
def suche_zutat():
    name = eingabe.get().strip()
    if not name:
        print("Error, Keine Zutat eingegeben")
        messagebox.showwarning("Hinweis", "Bitte gib eine Zutat ein.")
        return

    # API-Endpunkt für Cocktails, die eine bestimmte Zutat enthalten
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={name}"
    try:
        antwort = requests.get(url)
        daten = antwort.json()
    except Exception as e:
        print("Hinweis", f"API-Fehler:\n{e}")
        messagebox.showerror("Hinweis", f"API-Fehler:\n{e}")
        return

    liste.delete(0, tk.END)
    global ergebnisse, modus
    ergebnisse = daten.get("drinks")
    modus = "ingredient"

    if not ergebnisse:
        liste.insert(tk.END, "Keine Getränke mit dieser Zutat gefunden.")
        return

    # Liste der Drinks, die die Zutat enthalten
    for drink in ergebnisse:
        liste.insert(tk.END, drink["strDrink"])


# zeigt die Details des ausgewählten Eintrags in einem Dialogfenster an
def zeige_details(event=None):
    auswahl = liste.curselection()
    if not auswahl or not ergebnisse:
        return

    index = auswahl[0]
    eintrag = ergebnisse[index]

    # Wenn Cocktail-Modus aktiv ist, sind alle Infos bereits enthalten
    if modus == "cocktail":
        drink_id = eintrag.get("idDrink")
    else:
        # Wenn wir über eine Zutat gesucht haben, müssen wir Details per ID nachladen
        drink_id = eintrag.get("idDrink")

    if not drink_id:
        return

    # Details für den ausgewählten Drink abrufen
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}"
    try:
        antwort = requests.get(url)
        daten = antwort.json()
        drink = daten["drinks"][0]
    except Exception as e:
        messagebox.showerror("Fehler", f"Konnte Details nicht laden:\n{e}")
        return

    # Zutaten zusammenstellen
    zutaten = []
    for i in range(1, 16):
        zutat = drink.get(f"strIngredient{i}")
        menge = drink.get(f"strMeasure{i}")
        if zutat:
            zutaten.append(f"{zutat} - {menge or ''}")

    # Text für die Anzeige
    text = f"""
Name: {drink['strDrink']}
Kategorie: {drink.get('strCategory', 'Unbekannt')}
Alkoholisch: {drink.get('strAlcoholic', 'Unbekannt')}
Glas: {drink.get('strGlass', 'Unbekannt')}

Zutaten:
{chr(10).join(zutaten)}

Anleitung:
{drink.get('strInstructions', 'Keine Anleitung verfügbar.')}
    """

    messagebox.showinfo(f"Details zu {drink['strDrink']}", text.strip())


# --- GUI ---
root = tk.Tk()
root.title("Cocktail API")
root.geometry("500x420")

# Label und Eingabefeld
tk.Label(root, text="Cocktail oder Zutat suchen:", font=("Arial", 12, "bold")).pack(pady=10)
eingabe = tk.Entry(root, width=40)
eingabe.pack(pady=5)

# Buttons in einer Reihe
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Cocktail suchen", command=suche_cocktail,
          bg="#4CAF50", fg="white", width=18).grid(row=0, column=0, padx=5)

tk.Button(button_frame, text="Zutat suchen", command=suche_zutat,
          bg="#2196F3", fg="white", width=18).grid(row=0, column=1, padx=5)

# Listbox
liste = tk.Listbox(root, width=60, height=15)
liste.pack(pady=10)
liste.bind("<Double-Button-1>", zeige_details)

# Hinweistext
tk.Label(root, text="Doppelklick auf einen Cocktail für Details", fg="gray").pack()

# Variablen
ergebnisse = None
modus = "cocktail"

# Ereignisschleife starten
root.mainloop()
