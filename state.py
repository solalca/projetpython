import json

from gamerule import turn, free_case, convert_position, outofrange_move
from init import gridtab, charger_donnees, sauvegarder_donnees, datafile, letters
from phasedrone import drone_turnoff, dronechoice_count, dronemove, dronechoice, decrement_desactivation
from phasetempete import apply_storm_effect, stormchoice, stormmove

logfile = "data.json"
resultfile = "result.json"

journal = []

def show_state(turncount):
    data = charger_donnees()
    score = data.get("score", {"drones": 0, "tempetes": 0})
    print("\nEtat de la partie :")
    print(f"Tour {turncount}")
    print(f"Score - Drones: {score['drones']}, Tempêtes: {score['tempetes']}")
    print("Tour numéro :", turncount)
    for survivor in data.get("survivors", []):
        if survivor["alive"] and not survivor["saved"]:
            print(f"Survivant {survivor['id']} à la position {survivor['pos']}")

def gameloop():
    global journal
    journal = []  # reset journal
    turncount = 1
 
    while True:
        show_state(turncount)
        resultat = win_cond()
        if resultat:
            break
 
        if turncount % 2 == 1:
            print(f"\n-- Phase Drones (tour {turncount}) --")
            dronechoice_count()
        else:
            print(f"\n-- Phase Tempêtes (tour {turncount}) --")
            stormmove()
            apply_storm_effect()
 
        decrement_desactivation()
        turncount += 1
 
    # fin de partie
    donnees = charger_donnees()
    score = donnees.get("score", 0)
    print(f"=== FIN DE PARTIE === Vainqueur : {resultat} | Score final : {score}/10")
    with open(resultfile, "w", encoding="utf-8") as f:
        json.dump({"vainqueur": resultat, "score": score, "score_max": 10}, f, indent=4, ensure_ascii=False)

def win_cond():
    donnees = charger_donnees()
    all_saved = all(s["saved"] or not s["alive"] for s in donnees["survivants"])
    all_dead = all(d["etat"] == "desactive" or d["batterie"] == 0 for d in donnees["drones"])
    if all_saved:
        return "drones"
    if all_dead:
        return "tempetes"
    return None

if __name__ == "__main__":
    gameloop()