import json
from datetime import datetime, timedelta

class Lead:
    def __init__(self, nom, email, actions):
        self.nom = nom
        self.email = email
        self.actions = actions
        self.score = 0

    def calcul_score(self):
        try:
            self.score = 0
            for action in self.actions:
                type_action = action.get("type")
                date_action = action.get("date")


                try:
                    if date_action:
                        date_action = datetime.strptime(date_action,"%Y-%m-%d")
                except ValueError:
                    print(f"Date mal formatée pour {self.nom}, action ignorée.")
                    continue

                if type_action == "clic":
                    self.score += 20
                elif type_action == "telechargement":
                    self.score += 50
                elif type_action == "non_ouvert":
                    if date_action and (datetime.today() - date_action).days >= 30:
                        self.score -= 10

        except Exception as e:
            print(f"Erreur lors du calcul du score pour {self.nom}: {e}")
            self.score = 0

    def to_dict(self):
        return {
            "nom": self.nom,
            "email": self.email,
            "score": self.score,
            "actions": self.actions
        }

leads_data = [
    {
        "nom": "Alice",
        "email": "alice@email.com",
        "actions": [
            {"type": "clic", "date": "2026-01-15"},
            {"type": "telechargement", "date": "2026-01-16"}
        ]
    },
    {
        "nom": "Bob",
        "email": "bob@email.com",
        "actions": [
            {"type": "non_ouvert", "date": "2025-12-01"}
        ]
    },
    {
        "nom": "Charlie",
        "email": "charlie@email.com",
        "actions": [
            {"type": "clic", "date": "2026-02-01"},
            {"type": "non_ouvert", "date": "2025-12-01"}
        ]
    }
]

leads = []
for data in leads_data:
    lead = Lead(data["nom"], data["email"], data["actions"])
    lead.calcul_score()
    leads.append(lead)

leads_trie = sorted(leads, key=lambda x: x.score, reverse=True)


print("\nLEADS TRIÉS PAR SCORE\n")
for lead in leads_trie:
    print(f"{lead.nom} -------> {lead.email} ------> Score: {lead.score}\n")
print()

export_data = [lead.to_dict() for lead in leads_trie]

with open("leads_scores.json", "w") as f:
    json.dump(export_data, f, indent=4)

print("\nleads_scores.json est pret .")
