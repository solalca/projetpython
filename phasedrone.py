import json
import os
from init import charger_donnees, sauvegarder_donnees, datafile, letters, gridtab
from gamerule import turn, free_case, convert_position
    

def dronechoice():
    picker = input("Quel drone voulez-vous déplacer ? (ex: A1) : ")
    while convert_position(picker) is None:
        picker = input("Position invalide. Veuillez entrer une lettre suivie d'un chiffre : ")
    if gridtab[convert_position(picker)[0]-1][convert_position(picker)[1]-1] == 'D':
        dronecheck = json.loads(charger_donnees())["drones"]
        for drone in dronecheck:
            if convert_position(picker) == drone["pos"]:
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

