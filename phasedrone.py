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

def dronechoice():
    picker = input("Quel drone voulez-vous déplacer ? (ex: A1) : ")
    while convert_position(picker) is None:
        picker = input("Position invalide. Veuillez entrer une lettre suivie d'un chiffre : ")
    if gridtab[convert_position(picker)[0]-1][convert_position(picker)[1]-1] == 'D':
        dronecheck = json.loads(charger_donnees())["drones"]
        for drone in dronecheck:
            if convert_position(picker) == drone["pos"] or drone_turnoff() == True:
                if drone["bat"] != 0 and drone["status"] == False:
                    return convert_position(picker)
                else:
                    print("Ce drone n'est pas disponible. Veuillez en choisir un autre.")
                    return dronechoice()
    else:
        print("Pas de drone à cette position, choisir un autre drone.")
        return dronechoice()
    return convert_position(picker)

def dronemove():
    move = input("Où voulez-vous déplacer le drone ? (ex: A1) : ")
    while convert_position(move) is None:
        move = input("Position invalide. Veuillez entrer une lettre suivie d'un chiffre : ")
    chosendrone = dronechoice()
    if free_case(convert_position(move)) == False:
        print("Case déjà occupée, choisissez une autre case.")
        return dronemove()
    if outofrange_move(chosendrone, convert_position(move), chosendrone) == True:
        print("Déplacement hors de portée. Veuillez choisir une case adjacente.")
        return dronemove()
    else:
        dronecheck = json.loads(charger_donnees())["drones"]
        for drone in dronecheck:
            if chosendrone == drone["pos"]:
                gridtab[chosendrone[0]-1][chosendrone[1]-1] = "."
                drone["pos"] = convert_position(move)
                drone["bat"] -= 1
                sauvegarder_donnees(json.dumps({"drones": dronecheck}, indent=4))
                gridtab[convert_position(move)[0]-1][convert_position(move)[1]-1] = "D"
    return convert_position(move)

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

def drone_turnoff():
    dronecheck = json.loads(charger_donnees())["drones"]
    for drone in dronecheck:
        if dronebatchecker(drone) == False or drone["status"] == True:
            return True
    return False