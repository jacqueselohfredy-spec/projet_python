import pandas as pd

import os
FICHIER = input("Veuillez entrer le nom du fichier CSV : ")
if not FICHIER:
    print("Aucun fichier entré.")
else:

    if os.path.exists(FICHIER):
        df = pd.read_csv(FICHIER)
        print("Fichier chargé avec succès !")
        print(df.head())
    else:
        print("Le fichier n'existe pas.")

#Chargement des données "campagnes_emailing.csv"
#FICHIER = "campagnes_emailing.csv"

try:
    df = pd.read_csv(FICHIER)
except FileNotFoundError:
    print("Fichier non trouvé;\nGénération de données fictives")
    df = pd.DataFrame({
        "persona": ["Dirigeant", "Acheteur", "ETI", "PME"],
        "envoyes": [1000, 800, 500, 600],
        "ouvertures": [300, 200, 250, 180],
        "clics": [90, 40, 120, 30]
    })

# Remplacer les valeurs manquantes par 0
df.fillna(0, inplace=True)


colonnes_numeriques = ["envoyes", "ouvertures", "clics"]
df[colonnes_numeriques] = df[colonnes_numeriques].astype(int)


df = df[df["envoyes"] > 0]



df["taux_ouverture"] = (df["ouvertures"] / df["envoyes"]) * 100
df["ctr"] = (df["clics"] / df["envoyes"]) * 100
df["reactivite"] = (df["clics"] / df["ouvertures"]) * 100


df[["taux_ouverture", "ctr", "reactivite"]] = df[
    ["taux_ouverture", "ctr", "reactivite"]
].round(2)


meilleur_persona = df.sort_values(
    by="reactivite", ascending=False
).iloc[0]


print("\nRAPPORT DE PERFORMANCE")
print(f"Persona le plus engagé : {meilleur_persona['persona']}")
print(f"Taux d'ouverture : {meilleur_persona['taux_ouverture']} %")
print(f"CTR : {meilleur_persona['ctr']} %")
print(f"Réactivité : {meilleur_persona['reactivite']} %")

print("\nRecommandation business :")
print(
    f" Prioriser les prochaines campagnes sur le persona "
    f"{meilleur_persona['persona']}."
)

df_trie = df.sort_values(by="reactivite", ascending=False)
df_trie.to_csv("rapport_campagnes_optimise.csv", index=False)

print("\nrapport_campagnes_optimise.csv généré avec succès.")
