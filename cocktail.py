# Cocktail - API

print("Cocktail - API")

# Bibliotheken importieren
import requests


# Programm Code

# Nutzer nach dem Getränk fragen
drink = input("Welches Getränk möchtest du suchen? ")

# Variable in die URL einfügen
response = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}")

# Ausgabe (z.B. rohe JSON-Daten)
print(response.json())