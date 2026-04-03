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
gridsize = 12

gridtab = []
for i in range(gridsize):
    line = []
    for j in range(gridsize):
        line.append(".")
    gridtab.append(line)

def grid_display(gridtab):
    print("      " + " ".join(letters))
    for i in range(gridsize):
        content = " ".join(gridtab[i][j] for j in range(gridsize))
        print(f"{i+1:3}   {content}")     

#fonctions init
def init_drone():
    dronelist = []
    for i in range(6):
        a = int(random.randint(1,12))
        b = int(random.randint(1,12))
        drone = {
            "pos":(a,b),
            "bat":20,
            "status":False, #si status = false le drone pas capturé
            "loaded":False
        }
        gridtab[a-1][b-1] = "D"
        dronelist.append(drone)
    return(dronelist)

def init_tempete():
    tempetelist = []
    for i in range(4):
        a = int(random.randint(1,12))
        b = int(random.randint(1,12))
        tempete = {
            "pos":(a,b),
            "onelement":False, #si la tempete est sur un survivant ou sur un drone
        }
        gridtab[a-1][b-1] = "T"
        tempetelist.append(tempete)
        
    return(tempetelist)

def init_survivant():
    survlist = []
    for i in range(10):
        a = int(random.randint(1,12))
        b = int(random.randint(1,12))
        surv = {
            "pos":(a,b),
            "carried":False,
            "alive":True
        }
        gridtab[a-1][b-1] = "S"
        survlist.append(surv)
    return(survlist)

def hopital():
    a = int(random.randint(1,12))
    b = int(random.randint(1,12))
    hosto = {
        "pos":(a,b),
        "occupants":0,
    }
    gridtab[a-1][b-1] = "H"
    return(hosto)

def free_case():
    isfree = True
    for i in range(12):
        for j in range(12):
            if gridtab[i][j] != ".":
                isfree = False
            print(isfree)
    return(isfree)

free_case()

#sepadelia

hopital()
init_tempete()
init_drone()
init_survivant()
grid_display(gridtab)