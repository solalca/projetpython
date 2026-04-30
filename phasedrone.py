import json
import os
from init import charger_donnees, sauvegarder_donnees, datafile, letters, gridtab
from gamerule import turn, free_case, convert_position
    

def dronechoice():
    picker = input("Quel drone voulez-vous déplacer ? (ex: A1) : ")
    while convert_position(picker) is None:
        picker = input("Position invalide. Veuillez entrer une lettre suivie d'un chiffre : ")
    return convert_position(picker)

def dronemove():
    move = input("Où voulez-vous déplacer le drone ? (ex: A1) : ")
    while convert_position(move) is None:
        move = input("Position invalide. Veuillez entrer une lettre suivie d'un chiffre : ")
    return convert_position(move)

