import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class Lead:
    def __init__(self, nom, email, actions):
        self.nom = nom
        self.email = email
        self.actions = actions
        self.score = 0

    def calcul_score(self):
        self.score = 0

        for action in self.actions:
            type_action = action["type"]
            date_action = action["date"]

            try:
                date_action = datetime.strptime(date_action, "%Y-%m-%d")
            except:
                continue

            if type_action == "clic":
                self.score += 20

            elif type_action == "telechargement":
                self.score += 50

            elif type_action == "non_ouvert":
                if (datetime.today() - date_action).days >= 30:
                    self.score -= 10

    def to_dict(self):
        return {
            "nom": self.nom,
            "email": self.email,
            "score": self.score,
            "actions": self.actions
        }


leads = []
actions_temp = []



def ajouter_action():
    type_action = combo_action.get()
    date_action = entry_date.get()

    if not type_action or not date_action:
        messagebox.showwarning("Erreur", "Remplir action + date")
        return

    actions_temp.append({
        "type": type_action,
        "date": date_action
    })

    list_actions.insert(tk.END, f"{type_action} — {date_action}")
    entry_date.delete(0, tk.END)


def ajouter_lead():
    nom = entry_nom.get()
    email = entry_email.get()

    if not nom or not email or not actions_temp:
        messagebox.showwarning("Erreur", "Informations incomplètes")
        return

    lead = Lead(nom, email, actions_temp.copy())
    lead.calcul_score()
    leads.append(lead)

    actions_temp.clear()
    list_actions.delete(0, tk.END)

    entry_nom.delete(0, tk.END)
    entry_email.delete(0, tk.END)

    afficher_leads()


def afficher_leads():
    for row in tree.get_children():
        tree.delete(row)

    leads_trie = sorted(leads, key=lambda x: x.score, reverse=True)

    for lead in leads_trie:
        tree.insert("", tk.END, values=(lead.nom, lead.email, lead.score))


def exporter_json():
    data = [lead.to_dict() for lead in leads]

    with open("leads_scores.json", "w") as f:
        json.dump(data, f, indent=4)

    messagebox.showinfo("Succès", "Export JSON réussi !")



root = tk.Tk()
root.title("Lead Scorer Automatisé")
root.geometry("750x600")

tk.Label(root, text="Nom").pack()
entry_nom = tk.Entry(root)
entry_nom.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root)
entry_email.pack()


tk.Label(root, text="Type d'action").pack()

combo_action = ttk.Combobox(root, values=[
    "clic",
    "telechargement",
    "non_ouvert"
])
combo_action.pack()

tk.Label(root, text="Date (YYYY-MM-DD)").pack()
entry_date = tk.Entry(root)
entry_date.pack()

tk.Button(root, text="Ajouter action", command=ajouter_action).pack()

list_actions = tk.Listbox(root, height=5)
list_actions.pack(fill="x")


tk.Button(root, text="Ajouter Prospect", command=ajouter_lead,
          bg="green", fg="white").pack(pady=10)

tree = ttk.Treeview(root, columns=("Nom", "Email", "Score"),
                    show="headings")

tree.heading("Nom", text="Nom")
tree.heading("Email", text="Email")
tree.heading("Score", text="Score")

tree.pack(fill="both", expand=True)


tk.Button(root, text="Exporter JSON", command=exporter_json,
          bg="blue", fg="white").pack(pady=10)

root.mainloop()
