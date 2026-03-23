import string
import json
import os
import random

#data
datafile = "data.json"

def charger_donnees():
    if os.path.exists(datafile):
        with open(datafile, "r") as f:
            return json.load(f)
    return {}

def sauvegarder_donnees(donnees):
    with open(datafile, "w") as f:
        json.dump(donnees, f, indent=4)

# plateau
letters = "ABCDEFGHIJKL"
gridsize = 13
for i in range(gridsize):
    gridtab = []
    for j in range(gridsize):
        gridtab.append(".")
    print(gridtab)

def grid_display(gridsize):
    print("      " + "  ".join(letters))
    print()
    for i in range(gridsize):
        content = " ".join(gridtab[i][j] for j in range(gridsize))
        print(f"{i+1:3}   {content}")     


def init_drone(a,b):
    dronelist = []
    for i in range(6):
        a = int(input("Ligne du drone (1-12) : "))
        b = int(input("Colonne du drone (1-12) : "))
        drone = {
            "pos":(a,b),
            "bat":20,
            "status":False, #si status = false le drone pas capturé
            "loaded":False
        }
        dronelist.append(drone)
    return(dronelist)

def init_tempete(a,b):
    tempetelist = []
    for i in range(4):
        a = int(random.randint(1,12))
        b = int(random.randint(1,12))
        tempete = {
            "pos":(a,b),
            "onelement":False, #si la tempete est sur un survivant ou sur un drone
        }
        tempetelist.append(tempete)
    return(tempetelist)

def survivant(a,b):
    survlist = []
    for i in range(10):
        a = int(random.randint(1,12))
        b = int(random.randint(1,12))
        surv = {
            "pos":(a,b),
            "carried":False,
            "alive":True
        }
        survlist.append(surv)
    return(survlist)

