import json
import os
from init import charger_donnees, sauvegarder_donnees, datafile, letters, gridtab
from gamerule import outofrange_move, turn, free_case, convert_position
from phasedrone import drone_turnoff, dronemove
    

def stormchoice():
    picker = input("Quelle tempête voulez-vous déplacer ? (ex: A1) : ")
    pos = convert_position(picker)
    if pos is None:
        print("Position invalide.")
        return stormchoice()
    r, c = pos[0]-1, pos[1]-1
    if gridtab[r][c] != 'T':
        print("Pas de tempête à cette position.")
        return stormchoice()
    donnees = charger_donnees()
    for storm in donnees["storms"]:
        if storm["pos"] == list(pos):
            return pos
    print("Tempête introuvable.")
    return stormchoice()

def stormmove():
    for i in range(2):
        print(f"Tempête {i+1}/2")
        chosenst = stormchoice()
        move = input("Où voulez-vous déplacer la tempête ? (ex: B3) : ")
        pos = convert_position(move)
        if pos is None or outofrange_move(chosenst, pos):
            print("Position invalide ou hors de portée, tempête ignorée.")
            continue
        r, c = pos[0]-1, pos[1]-1
        if gridtab[r][c] == "B":
            print("Case bloquée, tempête ignorée.")
            continue
 
        donnees = charger_donnees()
        for storm in donnees["storms"]:
            if storm["pos"] == list(chosenst):
                gridtab[chosenst[0]-1][chosenst[1]-1] = "."
                storm["pos"] = list(pos)
                gridtab[r][c] = "T"
                apply_storm_effect(pos, donnees)
                break
        sauvegarder_donnees(donnees)

def apply_storm_effect(pos, donnees):
    r, c = pos[0]-1, pos[1]-1
    cell = gridtab[r][c]
    if cell == "D":
        drone_turnoff(pos)
        print(f"Collision ! Tempête en {pos} désactive un drone !")
    if cell == "S":
        for surv in donnees["survivants"]:
            if surv["pos"] == list(pos) and surv["alive"]:
                surv["alive"] = False
                gridtab[r][c] = "."
                print("Un survivant a été tué par la tempête !")
                break
    sauvegarder_donnees(donnees)


