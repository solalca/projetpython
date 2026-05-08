import json
import os
from shutil import move
from init import gridtab, charger_donnees, sauvegarder_donnees, letters

def turn():
    turncount = 1
    if turncount % 2 == 1:
        print("TOUR DRONE")
    else:
        print("TOUR TEMPETE")
    turncount += 1
    return(turncount)

def free_case():
    for i in range(len(gridtab)):
        for j in range(len(gridtab)):
            if gridtab[i][j] == ".":
                return True
            else:
                return False

def convert_position(userinput):
    userinput = userinput.upper().strip()
    if len(userinput) < 2 or len(userinput) > 3: #check si la position est bien ecrite
        print("Position invalide. Veuillez entrer une lettre suivie d'un chiffre.")
        return None
    else:
        col = userinput[0]
        lin = userinput[1:]
        while col not in letters:
                col = input("Lettre invalide. Veuillez entrer une lettre entre A et L : ").upper().strip()
        while not lin.isdigit() or int(lin) < 1 or int(lin) > 12:
                lin = input("Numéro de ligne invalide. Veuillez entrer un chiffre entre 1 et 12 : ").strip()
        return(int(lin), letters.index(col) + 1)

def outofrange_move(from_pos, to_pos):
    return abs(from_pos[0] - to_pos[0]) > 1 or abs(from_pos[1] - to_pos[1]) > 1
