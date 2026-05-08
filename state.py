import json

from gamerule import convert_position
from init import gridtab, charger_donnees, sauvegarder_donnees, grid_display
from phasedrone import dronechoice_count, decrement_desactivation
from phasetempete import stormmove

resultfile = "resultats.json"
LOG_FILE = "journal.json"
journal = []

def log(message):
    print(message)
    journal.append(message)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump({"journal": journal}, f, indent=4, ensure_ascii=False)

def show_state(turncount):
    data = charger_donnees()
    score = data.get("score", 0)
    survivants_restants = sum(1 for s in data["survivants"] if s["alive"] and not s["saved"])
    log(f"\n=== Tour {turncount} ===")
    grid_display(gridtab)
    log(f"Score : {score} | Survivants restants : {survivants_restants}")
    for i, drone in enumerate(data["drones"]):
        log(f"  D{i+1} pos={drone['pos']} batterie={drone['batterie']} état={drone['etat']} charge={drone['charge']}")

def win_cond():
    donnees = charger_donnees()
    all_saved = all(s["saved"] or not s["alive"] for s in donnees["survivants"])
    all_dead = all(d["etat"] == "desactive" or d["batterie"] == 0 for d in donnees["drones"])
    if all_saved:
        return "drones"
    if all_dead:
        return "tempetes"
    return None

def gameloop():
    global journal
    journal = []
    turncount = 1

    while True:
        show_state(turncount)
        resultat = win_cond()
        if resultat:
            break

        if turncount % 2 == 1:
            log(f"\n-- Phase Drones (tour {turncount}) --")
            dronechoice_count()
        else:
            log(f"\n-- Phase Tempêtes (tour {turncount}) --")
            stormmove()

        decrement_desactivation()
        turncount += 1

    donnees = charger_donnees()
    score = donnees.get("score", 0)
    log(f"=== FIN DE PARTIE === Vainqueur : {resultat} | Score final : {score}/10")
    with open(resultfile, "w", encoding="utf-8") as f:
        json.dump({"vainqueur": resultat, "score": score, "score_max": 10}, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    gameloop()