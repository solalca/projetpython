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
        while gridtab[a-1][b-1] != ".":
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

def init_storm():
    stormlist = []
    for i in range(4):
        a = int(random.randint(1,12))
        b = int(random.randint(1,12))
        while gridtab[a-1][b-1] != ".":
            a = int(random.randint(1,12))
            b = int(random.randint(1,12))
        storm = {
            "pos":(a,b),
            "onelement":False, #si la tempete est sur un survivant ou sur un drone
        }
        gridtab[a-1][b-1] = "T"
        stormlist.append(storm)
        
    return(stormlist)

def init_survivor():
    survlist = []
    for i in range(10):
        a = int(random.randint(1,12))
        b = int(random.randint(1,12))
        while gridtab[a-1][b-1] != ".":
            a = int(random.randint(1,12))
            b = int(random.randint(1,12))
        survivor = {
            "pos":(a,b),
            "carried":False,
            "alive":True,
            "saved":False
        }
        gridtab[a-1][b-1] = "S"
        survlist.append(survivor)
    return(survlist)

def hospital():
    a = int(random.randint(1,12))
    b = int(random.randint(1,12))
    while gridtab[a-1][b-1] != ".":
            a = int(random.randint(1,12))
            b = int(random.randint(1,12))
    hosto = {
        "pos":(a,b),
        "occupants":0,
    }
    gridtab[a-1][b-1] = "H"
    return(hosto)

def buildings():
    buildinglist = []
    for i in range(9):
        a = int(random.randint(1,12))
        b = int(random.randint(1,12))
        while gridtab[a-1][b-1] != ".":
                a = int(random.randint(1,12))
                b = int(random.randint(1,12))
        buildingspecs = {
            "pos":(a,b),
        }
        gridtab[a-1][b-1] = "B"
        buildinglist.append(buildingspecs)
    return(buildinglist)

#sepadelia

hosto = hospital()
storms = init_storm()
drones = init_drone()
survivants = init_survivor()
buildingdisp = buildings()
grid_display(gridtab)

for storm in storms:
    storm["pos"] = list(storm["pos"])

for survivor in survivants:
    survivor["pos"] = list(survivor["pos"])

for building in buildingdisp:
    building["pos"] = list(building["pos"])

hosto["pos"] = list(hosto["pos"])

for drone in drones:
    drone["batterie"] = drone.pop("bat")
    drone["etat"] = "actif"
    drone["charge"] = None
    drone["tours_desactive"] = 0
    drone.pop("status", None)
    drone.pop("loaded", None)

donnees = {
    "hospital": hosto,
    "storms": storms,
    "drones": drones,
    "survivants": survivants,
    "buildings": buildingdisp,
    "grid": gridtab,
    "score": 0
}



sauvegarder_donnees(donnees)