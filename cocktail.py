# Cocktail - API

print("Cocktail - API")

# Bibliotheken importieren
import requests


# Programm Code

response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=Margarita")
data = response.json()
print(data)