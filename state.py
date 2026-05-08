from gamerule import turn, free_case, convert_position, outofrange_move
from init import gridtab, charger_donnees, sauvegarder_donnees, datafile, letters
from phasedrone import drone_turnoff, dronechoice_count, dronemove, dronechoice
from phasetempete import storm_effect, stormchoice, stormmove

def gameloop():
    if turn() %2 == 1: #tour drone
        print("TOUR DRONE")
        dronechoice()
        dronemove()
        dronechoice_count()
    else: #tour tempete
        print("TOUR TEMPETE")
        stormchoice()
        stormmove()
        storm_effect()

def win_cond():
    survcheck = json.loads(charger_donnees())["survivors"]
    for survivor in survcheck:
        if survivor["saved"] == True:
            print("victoire des drones")
            return True
    
        print("victoire de la tempete")
    return False