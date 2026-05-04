import json
import os
from init import charger_donnees, sauvegarder_donnees, datafile, letters, gridtab
from gamerule import turn, free_case, convert_position
from phasedrone import dronemove
    

def stormchoice():
    picker = input("Quel drone voulez-vous déplacer ? (ex: A1) : ")
    while convert_position(picker) is None:
        picker = input("Position invalide. Veuillez entrer une lettre suivie d'un chiffre : ")
    if gridtab[convert_position(picker)[0]-1][convert_position(picker)[1]-1] == 'D':
        stormcheck = json.loads(charger_donnees())["tempetes"]
        for storm in stormcheck:
            return convert_position(picker)
    else:
        print("Pas de tempête à cette position, choisir une autre tempête.")
        return stormchoice()
    return convert_position(picker)

def stormmove():
    move = input("Où voulez-vous déplacer la tempête ? (ex: A1) : ")
    while convert_position(move) is None:
        move = input("Position invalide. Veuillez entrer une lettre suivie d'un chiffre : ")
    chosenstorm = stormchoice()
    if free_case(convert_position(move)) == False:
        print("Case déjà occupée, choisissez une autre case.")
        return stormmove()
    else:
        stormcheck = json.loads(charger_donnees())["tempetes"]
        for storm in stormcheck:
            if chosenstorm == storm["pos"]:
                gridtab[chosenstorm[0]-1][chosenstorm[1]-1] = "."
                storm["pos"] = convert_position(move)
                sauvegarder_donnees(json.dumps({"tempetes": stormcheck}, indent=4))
                gridtab[convert_position(move)[0]-1][convert_position(move)[1]-1] = "D"
    return convert_position(move)

