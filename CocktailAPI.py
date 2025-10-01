import tkinter as tk
from tkinter import ttk, messagebox
import requests

API = "https://www.thecocktaildb.com/api/json/v1/1/"

def search_by_name(name):
    url = API + f"search.php?s={name}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get("drinks")

def filter_by_ingredient(ingredient):
    url = API + f"filter.php?i={ingredient}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get("drinks")

def lookup_cocktail(id_):
    url = API + f"lookup.php?i={id_}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get("drinks")

class CocktailApp:
    def __init__(self, root):
        self.root = root
        root.title("Cocktail-Suche")

        # Eingabe & Buttons
        frame = ttk.Frame(root)
        frame.pack(padx=10, pady=10, fill="x")

        self.entry = ttk.Entry(frame)
        self.entry.pack(side="left", fill="x", expand=True)
        self.search_name_btn = ttk.Button(frame, text="Nach Name", command=self.on_search_name)
        self.search_name_btn.pack(side="left", padx=5)
        self.search_ing_btn = ttk.Button(frame, text="Nach Zutat", command=self.on_search_ing)
        self.search_ing_btn.pack(side="left")

        # Ergebnis-Liste
        self.result_list = tk.Listbox(root, height=10)
        self.result_list.pack(padx=10, pady=5, fill="both", expand=True)
        self.result_list.bind("<<ListboxSelect>>", self.on_select)

        # Detail-Text
        self.detail_text = tk.Text(root, height=10, wrap="word")
        self.detail_text.pack(padx=10, pady=5, fill="both", expand=True)

        self.current_results = []  # speichert die aktuelle Ergebnisliste

    def on_search_name(self):
        query = self.entry.get().strip() 
        if not query:
            messagebox.showinfo("Hinweis", "Bitte einen Namen eingeben.")
            return
        try:
            drinks = search_by_name(query)
            self.show_results(drinks)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Suche: {e}")

    def on_search_ing(self):
        query = self.entry.get().strip()
        if not query:
            messagebox.showinfo("Hinweis", "Bitte eine Zutat eingeben.")
            return
        try:
            drinks = filter_by_ingredient(query)
            self.show_results(drinks)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Suche: {e}")

    def show_results(self, drinks):
        self.result_list.delete(0, tk.END)
        self.current_results = []
        self.detail_text.delete(1.0, tk.END)
        if drinks is None:
            messagebox.showinfo("Keine Ergebnisse", "Es wurden keine Cocktails gefunden.")
            return
        for d in drinks:
            name = d.get("strDrink")
            self.result_list.insert(tk.END, name)
            self.current_results.append(d)

    def on_select(self, event):
        sel = self.result_list.curselection()
        if not sel:
            return
        idx = sel[0]
        drink = self.current_results[idx]
        # Hole vollstaendige Details via lookup
        full = lookup_cocktail(drink.get("idDrink"))
        if full:
            detail = full[0]
            self.show_detail(detail)

    def show_detail(self, detail):
        self.detail_text.delete(1.0, tk.END)
        sb = []
        sb.append(f"Name: {detail.get('strDrink')}")
        sb.append(f"Category: {detail.get('strCategory')}")
        sb.append(f"Glas: {detail.get('strGlass')}")
        sb.append("Zutaten:")
        # Zutaten & Mengen: strIngredient1 strMeasure1 
        for i in range(1, 16):  # max 15 Zutaten 
            ingr = detail.get(f"strIngredient{i}")
            meas = detail.get(f"strMeasure{i}")
            if ingr and ingr.strip():
                line = ingr
                if meas and meas.strip():
                    line += f" — {meas.strip()}"
                sb.append("  " + line)
        sb.append("\nAnleitung:")
        sb.append(detail.get("strInstructions", ""))
        text = "\n".join(sb)
        self.detail_text.insert(tk.END, text)


if __name__ == "__main__":
    root = tk.Tk()
    app = CocktailApp(root)
    root.mainloop()
