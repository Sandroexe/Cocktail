# Bibliotheken importieren - Vorher pip Install!!!
import tkinter as tk                     # GUI-Bibliothek (eingebautes Tkinter)
from tkinter import messagebox            # einfache Dialoge (Info/Fehler/Warnung)
import requests                           # HTTP-Anfragen an die Cocktail-API

# Funktionen definieren

# Cocktail-Datenbank durchsuchen
def suche_cocktail():
    # Lese Eingabe aus dem Eingabefeld und bereinigen von Leerzeichen (vorne und hinten)
    name = eingabe.get().strip()
    if not name:
        # Kurze Konsoleausgabe und Warn-Dialog, falls kein Name eingegeben wurde
        print("Hinweis", "Bitte gib einen Cocktailnamen ein.")
        messagebox.showwarning("Hinweis", "Bitte gib einen Cocktailnamen ein.")
        return


    # URL für die API vorbereiten bzw. in variabl speichrn
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"


    try:
        # Anfrage senden und als json in daten zwischenspeichern
        antwort = requests.get(url)
        daten = antwort.json()
    except Exception as e:
        # Fehlermeldung für Probleme der API ("Internetprobleme")
        print("Hinweis", f"API-Fehler:\n{e}")
        messagebox.showerror("Hinweis", f"API-Fehler:\n{e}")
        return

    # Vorherige Listeneinträge entfernen
    liste.delete(0, tk.END)
    # Ergebnis globalisieren (Tipp aus dem Internet, vermeidet Kopfschmerzen) um über andere Varbeln zugriff zu erhalten
    global ergebnisse, modus
    ergebnisse = daten.get("drinks")
    modus = "cocktail"

    # Falls keine Treffer, entsprechende Nachricht in die Listbox schreiben
    if not ergebnisse:
        liste.insert(tk.END, "Keine Ergebnisse gefunden.")
        return

    # Gefundene Cocktails als Namen in die Listbox einfügen
    for drink in ergebnisse:
        liste.insert(tk.END, drink["strDrink"])


# ZutatDatenbank nach Zutaten durchsuchern
def suche_zutat():
    # Eingegebene Zutat auslesn und "formatieren"
    name = eingabe.get().strip()
    if not name:
        # Mal wieder warnmeldung wenn nix eingegeben wurde. (Eventuell spätr in 1 funktion haun)
        print("Error, Keine Zutat eingegeben")
        messagebox.showwarning("Hinweis", "Bitte gib eine Zutat ein.")
        return

    # API-URL für Zutaten Filterung aufrugfn
    # Gleich wie vorhin mit "Fehleranalyse"
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={name}"
    try:
        antwort = requests.get(url)
        daten = antwort.json()
    except Exception as e:
        # Netzwerk/API Fehler melden
        print("Hinweis", f"API-Fehler:\n{e}")
        messagebox.showerror("Hinweis", f"API-Fehler:\n{e}")
        return

    # Alte Einträge löschen und Ergebnisse speichern
    liste.delete(0, tk.END)
    global ergebnisse, modus
    ergebnisse = daten.get("drinks")
    modus = "ingredient"

    # Keine Getränke mit dieser Zutat gefunden
    if not ergebnisse:
        liste.insert(tk.END, "Keine Getränke mit dieser Zutat gefunden.")
        return

    # Namen der Drinks in die Listbox einfügen
    for drink in ergebnisse:
        liste.insert(tk.END, drink["strDrink"])


# zeigt die Details des ausgewählten Eintrags in einem Dialogfenster an
def zeige_details(event=None):
    # Index der aktuellen Auswahl in der Listbox
    auswahl = liste.curselection()
    # Keine Auswahl oder keine geladenen Ergebnisse -> abbrechen
    if not auswahl or not ergebnisse:
        return

    index = auswahl[0]
    eintrag = ergebnisse[index]

    # Unabhängig vom Modus wird die ID des Drinks benötigt
    if modus == "cocktail":
        drink_id = eintrag.get("idDrink")
    else:
        # Bei Zutaten-Suche enthält das Ergebnis nur Basisinfos, ID ist ebenfalls vorhanden
        drink_id = eintrag.get("idDrink")

    if not drink_id:
        # Falls keine ID vorliegt, nichts tun
        return

    # Detail-API aufrufen, um vollständige Informationen (Zutaten, Anleitung) zu erhalten
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}"
    try:
        antwort = requests.get(url)
        daten = antwort.json()
        drink = daten["drinks"][0]    # erstes (und einziges) Ergebnis
    except Exception as e:
        # Fehler beim Laden der Details anzeigen
        messagebox.showerror("Fehler", f"Konnte Details nicht laden:\n{e}")
        return

    # Zutaten und Mengen zusammenstellen (API liefert bis zu 15 Zutatenfelder)
    zutaten = []
    for i in range(1, 16):
        zutat = drink.get(f"strIngredient{i}")
        menge = drink.get(f"strMeasure{i}")
        if zutat:
            # Menge kann None sein
            zutaten.append(f"{zutat} - {menge or ''}")

    # Info-Text formatieren (Name, Kategorie, Glas, Zutaten, Anleitung)
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

    # Details in einem Info-Dialog anzeigen
    messagebox.showinfo(f"Details zu {drink['strDrink']}", text.strip())


# --- GUI ---
root = tk.Tk()                             # Hauptfenster erstellen
root.title("Cocktail API")                 # Fenstertitel
root.geometry("500x420")                   # Fenstergröße

# Label und Eingabefeld für Suche
tk.Label(root, text="Cocktail oder Zutat suchen:", font=("Arial", 12, "bold")).pack(pady=10)
eingabe = tk.Entry(root, width=40)
eingabe.pack(pady=5)

# Buttons in einer Reihe (Frame zur Anordnung)
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Button: Suche nach Cocktailname
tk.Button(button_frame, text="Cocktail suchen", command=suche_cocktail,
          bg="#4CAF50", fg="white", width=18).grid(row=0, column=0, padx=5)

# Button: Suche nach Zutat
tk.Button(button_frame, text="Zutat suchen", command=suche_zutat,
          bg="#2196F3", fg="white", width=18).grid(row=0, column=1, padx=5)

# Listbox für Suchergebnisse (Liste der Drink-Namen)
liste = tk.Listbox(root, width=60, height=15)
liste.pack(pady=10)
# Doppelklick auf ein Listbox-Element zeigt die Details an
liste.bind("<Double-Button-1>", zeige_details)

# Kleiner Hinweis unterhalb der Liste
tk.Label(root, text="Doppelklick auf einen Cocktail für Details", fg="gray").pack()

# Initiale Variablen: keine Ergebnisse, Standardmodus 'cocktail'
ergebnisse = None
modus = "cocktail"

# Ereignisschleife starten (GUI aktiv halten)
root.mainloop()
