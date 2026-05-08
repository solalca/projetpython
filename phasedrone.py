import json
import os
from shutil import move
from init import charger_donnees, sauvegarder_donnees, datafile, letters, gridtab
from gamerule import turn, free_case, convert_position, outofrange_move
    
dronepick_count = 0

def dronechoice_count():
    while dronepick_count < 3:
        if dronechoice.picker == "exit":
            print("Fin de la phase drone")
            break
        else:
            dronechoice()
            dronemove()
        dronepick_count += 1
    return dronepick_count

def decrement_desactivation(): #change les compteurs de désactivation des drones et les réactive si nécessaire
    donnees = charger_donnees()
    for drone in donnees["drones"]:
        if drone["etat"] == "desactive":
            drone["tours_desactive"] -= 1
            if drone["tours_desactive"] <= 0:
                drone["etat"] = "actif"
                drone["tours_desactive"] = 0
                print(f"Drone en {drone['pos']} réactivé !")
    sauvegarder_donnees(donnees)


def dronechoice():
    picker = input("Quel drone voulez-vous déplacer ? (ex: A1, ou 'fin' pour terminer) : ")
    if picker.lower() == "fin":
        return None
    pos = convert_position(picker)
    if pos is None:
        print("Position invalide.")
        return dronechoice()
    r, c = pos[0]-1, pos[1]-1
    if gridtab[r][c] != 'D':
        print("Pas de drone à cette position.")
        return dronechoice()
    donnees = charger_donnees()
    for drone in donnees["drones"]:
        if drone["pos"] == list(pos):
            if drone["etat"] == "desactive":
                print("Ce drone est désactivé.")
                return dronechoice()
            if drone["batterie"] == 0:
                print("Ce drone n'a plus de batterie.")
                return dronechoice()
            return pos
    print("Drone introuvable.")
    return dronechoice()

def dronemove(chosendrone):
    move = input("Où voulez-vous déplacer le drone ? (ex: B3) : ")
    pos = convert_position(move)
    if pos is None:
        print("Position invalide.")
        return dronemove(chosendrone)
    if outofrange_move(chosendrone, pos):
        print("Déplacement hors de portée (1 case max, diagonal autorisé).")
        return dronemove(chosendrone)
    r, c = pos[0]-1, pos[1]-1
    cell = gridtab[r][c]
    if cell == "B":
        print("Case bloquée par un bâtiment.")
        return dronemove(chosendrone)
    if cell == "T":
        print("Case occupée par une tempête — le drone sera désactivé !")
 
    donnees = charger_donnees()
    score = donnees.get("score", 0)
 
    for drone in donnees["drones"]:
        if drone["pos"] == list(chosendrone):
            # déplacement sur la grille
            gridtab[chosendrone[0]-1][chosendrone[1]-1] = "."
            drone["pos"] = list(pos)
 
            # coût batterie
            if drone["charge"] is not None:
                drone["batterie"] = max(0, drone["batterie"] - 2)
            else:
                drone["batterie"] = max(0, drone["batterie"] - 1)
 
            # collision avec tempête
            if cell == "T":
                drone["etat"] = "desactive"
                drone["tours_desactive"] = 2
 
            # récupération survivant
            for surv in donnees["survivants"]:
                if surv["pos"] == list(pos) and not surv["carried"] and surv["alive"]:
                    surv["carried"] = True
                    drone["charge"] = "S"
                    gridtab[r][c] = "D"
                    print("Survivant récupéré !")
                    break
 
            # dépôt à l'hôpital
            if cell == "H" or donnees["hospital"]["pos"] == list(pos):
                gridtab[r][c] = "H"
                if drone["charge"] is not None:
                    for surv in donnees["survivants"]:
                        if surv["carried"] and surv["alive"]:
                            surv["carried"] = False
                            surv["saved"] = True
                            surv["alive"] = False
                            score += 1
                            drone["charge"] = None
                            print(f"Survivant sauvé ! Score : {score}")
                            break
                # recharge batterie sur hôpital
                drone["batterie"] = min(20, drone["batterie"] + 3)
            else:
                gridtab[r][c] = "D"
 
            break
 
    donnees["score"] = score
    sauvegarder_donnees(donnees)
    return pos

def dronebatchecker(drone):
    if drone["bat"] == 0:
        print("Le drone est à court de batterie et ne peut plus être déplacé.")
        return False
    return True

def drone_saving():
    dronecheck = json.loads(charger_donnees())["drones"]
    survivorcheck = json.loads(charger_donnees())["survivors"]
    for drone in dronecheck:
        for survivor in survivorcheck:
            if drone["pos"] == survivor["pos"] and survivor["carried"] == False and survivor["alive"] == True:
                survivor["carried"] = True
                drone["status"] = True
                sauvegarder_donnees(json.dumps({"drones": dronecheck, "survivors": survivorcheck}, indent=4))
                print("Survivant sauvé !")

def drone_drop():
    if gridtab[convert_position(move)[0]-1][convert_position(move)[1]-1] == "H":
        survcheck = json.loads(charger_donnees())["survivors"]
        for survivor in survcheck:
            if survivor["carried"] == True and survivor["alive"] == True:
                survivor["carried"] = False
                survivor["saved"] = True
                survcheck.remove(survivor)
                sauvegarder_donnees(json.dumps({"survivors": survcheck}, indent=4))
                print("Survivant déposé à l'hôpital !")

def drone_turnoff(pos):
    donnees = charger_donnees()
    for drone in donnees["drones"]:
        if drone["pos"] == list(pos):
            drone["etat"] = "desactive"
            drone["tours_desactive"] = 2
            print(f"Drone en {pos} désactivé pour 2 tours !")
    sauvegarder_donnees(donnees)

def dronechoice_count():
    global dronepick_count
    dronepick_count = 0
    moves = 0
    while moves < 3:
        print(f"Déplacement {moves+1}/3 (tapez 'fin' pour passer)")
        chosendrone = dronechoice()
        if chosendrone is None:
            break
        dronemove(chosendrone)
        moves += 1