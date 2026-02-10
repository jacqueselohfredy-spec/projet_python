import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# Fonction pour charger le fichier CSV
def charger_fichier():
    global df
    FICHIER = filedialog.askopenfilename(
        title="Sélectionner un fichier CSV",
        filetypes=[("Fichiers CSV", "*.csv")]
    )

    if not FICHIER:
        messagebox.showwarning("Avertissement", "Aucun fichier sélectionné.")
        return

    try:
        df = pd.read_csv(FICHIER)
        messagebox.showinfo("Succès", "Fichier chargé avec succès !")
        traiter_donnees()
        afficher_tableau()
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier non trouvé.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire le fichier.\n{e}")


# Fonction pour calculer les indicateurs et afficher les résultats
def traiter_donnees():
    global df
    # Remplacer les valeurs manquantes par 0
    df.fillna(0, inplace=True)

    colonnes_numeriques = ["envoyes", "ouvertures", "clics"]
    for col in colonnes_numeriques:
        if col not in df.columns:
            df[col] = 0
    df[colonnes_numeriques] = df[colonnes_numeriques].astype(int)

    df = df[df["envoyes"] > 0]

    # Calcul des KPI
    df["taux_ouverture"] = (df["ouvertures"] / df["envoyes"]) * 100
    df["ctr"] = (df["clics"] / df["envoyes"]) * 100
    df["reactivite"] = (df["clics"] / df["ouvertures"].replace({0: 1})) * 100

    df[["taux_ouverture", "ctr", "reactivite"]] = df[
        ["taux_ouverture", "ctr", "reactivite"]
    ].round(2)

    # Meilleur persona
    meilleur_persona = df.sort_values(by="reactivite", ascending=False).iloc[0]

    result_text.set(
        f"Persona le plus engagé : {meilleur_persona['persona']}\n"
        f"Taux d'ouverture : {meilleur_persona['taux_ouverture']} %\n"
        f"CTR : {meilleur_persona['ctr']} %\n"
        f"Réactivité : {meilleur_persona['reactivite']} %\n\n"
        f"Recommandation : Prioriser les prochaines campagnes sur le persona {meilleur_persona['persona']}."
    )

    # Sauvegarder le rapport
    df_trie = df.sort_values(by="reactivite", ascending=False)
    df_trie.to_csv("rapport_campagnes_optimise.csv", index=False)
    messagebox.showinfo("Succès", "rapport_campagnes_optimise.csv généré avec succès.")


# Fonction pour afficher le DataFrame dans le Treeview
def afficher_tableau():
    global df
    # Nettoyer le tableau précédent
    for i in tree.get_children():
        tree.delete(i)

    # Définir les colonnes
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Ajouter les lignes
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))


# Création de l'interface Tkinter
root = tk.Tk()
root.title("Analyse de campagnes Emailing")
root.geometry("900x600")

# Bouton pour charger le fichier
btn_charger = tk.Button(root, text="Charger un fichier CSV", command=charger_fichier)
btn_charger.pack(pady=10)

# Zone pour afficher les résultats
result_text = tk.StringVar()
lbl_result = tk.Label(root, textvariable=result_text, justify="left", font=("Arial", 12))
lbl_result.pack(padx=10, pady=10)

# Frame pour le tableau avec scrollbar
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=10, pady=10)

scrollbar_y = tk.Scrollbar(frame_table, orient="vertical")
scrollbar_y.pack(side="right", fill="y")

scrollbar_x = tk.Scrollbar(frame_table, orient="horizontal")
scrollbar_x.pack(side="bottom", fill="x")

tree = ttk.Treeview(frame_table, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
tree.pack(fill="both", expand=True)

scrollbar_y.config(command=tree.yview)
scrollbar_x.config(command=tree.xview)

root.mainloop()
