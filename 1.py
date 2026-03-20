<<<<<<< HEAD
import string
import json
import os

#data
datafile = "data.json"

def charger_donnees():
    if os.path.exists(FICHIER):
        with open(FICHIER, "r") as f:
            return json.load(f)
    return {}

def sauvegarder_donnees(donnees):
    with open(FICHIER, "w") as f:
        json.dump(donnees, f, indent=4)

# plateau
header = "   " + " ".join(string.ascii_uppercase[:12])
print(header)

for i in range(1, 13):
    ligne = ["."] * 12
    numero = str(i).ljust(2)
    print(numero + " " + " ".join(ligne))

def drone(a,b):
    print("COORDONNEES DU DRONE : ")
    a = int(input("Ligne : "))
    b = int(input("Colonne : "))
    donnees = charger_donnees()
    donnees["drone"] = {"ligne": a, "colonne": b}
    sauvegarder_donnees(donnees)
    return(a,b)
=======
import string

# plateau
header = "   " + " ".join(string.ascii_uppercase[:12])
print(header)

for i in range(1, 13):
    ligne = ["."] * 12
    numero = str(i).ljust(2)
    print(numero + " " + " ".join(ligne))

#def drone(a,b):
>>>>>>> 39c7b5fa9096c7b31564d8475fdccf8598be27e4
