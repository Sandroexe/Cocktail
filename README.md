# Cocktail-API + Tkinter

Ein Python-Projekt welches mit grafischer Oberfläche (GUI), das über die **TheCocktailDB-API** Cocktails und deren Zutaten suchen kann.  
Erstellt mit **Tkinter** (Standard-GUI-Bibliothek von Python) und **requests** für den Internetzugriff.

---

## 📋 Beschreibung

Dieses Programm ermöglicht es, Cocktails entweder **nach Namen** oder **nach Zutaten** zu suchen.  
Die Ergebnisse werden in einer **Liste** angezeigt, und durch einen **Doppelklick** auf einen Cocktail werden **Details** (Zutaten, Menge, Glasart und Anleitung) angezeigt.

Die Daten stammen von der öffentlichen API:  
👉 [https://www.thecocktaildb.com/api.php](https://www.thecocktaildb.com/api.php)

---

## 🧩 Funktionen

- **Cocktail-Suche:**  
  Suche nach Cocktails anhand des Namens (z. B. "Margarita").
  
- **Zutatensuche:**  
  Suche nach allen Cocktails, die eine bestimmte Zutat enthalten (z. B. "Gin").
  
- **Detailanzeige:**  
  Zeigt auf Doppelklick alle Informationen zu einem ausgewählten Cocktail (Name, Kategorie, Glas, Zutaten, Anleitung).

- **Fehlerbehandlung:**  
  - Warnung, wenn keine Eingabe gemacht wurde  
  - Fehlermeldung, wenn die API nicht erreichbar ist  
  - Hinweis, wenn keine Ergebnisse gefunden wurden

---

## 🛠️ Voraussetzungen

Bevor das Programm gestartet wird, müssen eventuell benötigte Bibliotheken installiert werden.

**Wichtig:**  
`tkinter` ist normalerweise **bereits in Python enthalten**.  
`requests` muss eventuell noch installiert werden.

```bash
pip install requests
