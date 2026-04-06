import json
import os
from init import charger_donnees, sauvegarder_donnees, datafile, letters, gridtab

def convert_letters(letters):
    return [ord(letter) - 64 for letter in letters] #ord => convertit la lettre en son emplacement ascii

convert_letters(letters)


def droneplay():
    for i in range(3):
        selected_drone = int(input("Sélectionnez la position du drone que vous déplacez : "))
        if gridtab[i][j] == D:
            #logique de placement
            pass
        else:
            print("Case déjà occupée")
            while gridtab[i][j]:
                selected_drone = int(input("Sélectionnez la position du drone que vous déplacez : "))
        selected_newposition = int(input("Sélectionnez la nouvelle position du drone : "))
        