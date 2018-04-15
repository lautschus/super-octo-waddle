from room import Room
from planet import Planet, River, Mill, House
from player import Player
from monster import Monster
import time
from items import *
import ships
import sys
import os
import updater
import random
import subprocess
import pickle

#gets working directory in order to save
currentos = sys.platform
if currentos == "win32":
    savePath = os.getcwd()+"\saves"
else:
    savePath = os.getcwd()+"/saves"
saveDir = os.listdir(savePath)
updates = updater.updates
player = Player(updates)
worlds = []

#Imports matplotlib if necessary
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches    
except ImportError:
    subprocess.run("python -mpip install -U pip")
    subprocess.run("python -mpip install -U matplotlib")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches        

def save(currentos):#Saves it as a .dat file using pickle. 
    #store the main variables that run the game, the player, the planets, and the update list.
    name = input("What is your name? ").lower()
    saveName = name+".dat"
    if currentos == "win32":
        with open(savePath+'\\'+saveName, 'wb') as f:
            pickle.dump([player, worlds, updates], f, protocol=2)
    else:
        with open(savePath+'//'+saveName, 'wb') as f:
            pickle.dump([player, worlds, updates], f, protocol=2)
        
def selectDifficulty():
    print("Easy")
    print("Medium")
    print("Hard")
    planets = None
    while planets is None:
        level = input("What difficulty? ")
        if level.lower() == "easy":
            planets = 3
        if level.lower() == "medium":
            planets = 6
        if level.lower() == "hard":
            planets = 9
    return planets

def createWorld():
    planets = selectDifficulty()
    for i in range(planets):
        worlds.append(Planet("Planet-"+str(i),"Welcome to "+"Planet-"+str(i),i*random.randint(0,100),updates))
    for i in worlds:     
        numberOfTrees = random.randint(0,100)
        for j in range(numberOfTrees):
            tree = Tree.Tree(updates)
            tree.putInRoom(i)
        if random.random()>.5:
            river = River(i,updates)
            i.addLocation(river)

    player.location = worlds[0]
    player.ship = ships.Ship(player,updates)

    #return jim to his house on planet 0
    jim = Jim.Jim(updates)
    jim.putInRoom(worlds[random.randint(1,planets-1)])
    jimsHouse = House('An empty house','You see a handful of red vines on the windowsill',player,updates)
    worlds[0].addLocation(jimsHouse)
    jimBait = RedVines.RedVines(updates)
    jimBait.putInRoom(jimsHouse)
    jimsHouse.key.putInRoom(worlds[0])
            
        
    i = Rock.Rock(updates)
    i.putInRoom(worlds[0])
        

def Load(currentos):
    clear()
    global player
    global worlds
    global updates
    completed = False
    while not completed:
        for i in saveDir:
            if i == "__init__.py":
                pass
            else:
                print(i)
        name = input("Type the name of the file youd like to load, or type none if you do not want to. ").lower()
        if name == "none":
            createWorld()
            completed = True
        elif name in saveDir:
            if currentos == "win32":
                with open(savePath+"\\"+name, 'rb') as f:
                    player, worlds,updates = pickle.load(f)
            else:
                with open(savePath+"//"+name, 'rb') as f:
                    player, worlds,updates = pickle.load(f)
            completed = True
        else:
            input("Invalid response, press enter to continue.")
    

def checkForSave():
    hasSave = False
    for i in saveDir:
        if ".dat" in i:
            hasSave = True
        
    if hasSave:
        answer = input("Would you like to load a previous save? Y/N ").lower()
        if answer in ["yes","y","ye","yess"]:
            Load(currentos)
            
        else:
            createWorld()
    else:
        input("No save, creating new game.")
        createWorld()
          
    

def map(location):
    if location == "planets":
        xvals = []
        yvals = []
        for i in worlds:
            xvals.append(i.x)
            yvals.append(i.y)
        plt.plot(xvals, yvals, 'ro')
        for i in worlds:
            if i is player.location:
                plt.annotate("You are here!",(i.x,i.y))
            else:
                plt.annotate(i.name,(i.x,i.y))
        plt.show()
        input("Press Enter to Continue")
    elif location.type == "house":
        input("Once I figure out how to graph squares you can have your map.")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def printSituation():
    clear()
    print(player.location.desc)
    print()
    if player.location.hasMonsters():
        print("This "+player.location.type+" contains the following monsters:")#print proper location type
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.hasItems():
        print("This "+player.location.type+" contains the following items:")#makes sure it prints the proper location type
        for i in player.location.items:
            if player.location.items[i][0]>0:
                print(i+" x "+str(player.location.items[i][0]))
        print()
    if player.location.type == "planet":  
    #if the player is outside on a planet, they can see what other planets to go to.
        print("Available Planets:")
    # for e in player.location.exitNames():
        # print(e)
        for i in worlds:
            if i == player.location:
                pass
            else:
                print("Distance to "+i.name+": "+str(player.location.distanceTo(i)))#prints distance from current planet to each other planet
        print()
        print("On Planet Destinations: ")
        #lists the buildings on the planet
        for i in player.location.locations:
            print(i.name)
        print()
        #prints information about the ship
        print("Current Location: "+player.location.name)
        print("Fuel: "+str(player.ship.currentFuel))
        print("Fuel used to takeoff: "+str(player.ship.takeOff))
        print("Fuel Efficieny: "+str(player.ship.fuelEfficieny))
    elif player.location.type == "house":
    #if the player is indoors, it lists the rooms in the building
        print("Type outside to leave")
        print("Rooms:")
        for i in player.location.locations:
            print(i.name)
    elif player.location.type == "river":
        print("You are next to the river.")
        mills = player.location.locations
        print("Mills: ")
        print()
        if len(mills) == 0:
            millReport = 'This river has no mills.'
        else:
            for i in mills:
                print(i.name)
                



    print()

def showHelp():
    clear()
    print("flyto <planet> -- fly to that planet")
    print("walkto <location> -- walk to on planet desitnation.")
    print("pickup <item> -- picks up the item")
    print("pickup <item> <number> -- will ask how many of <item> you want to pick up.")
    print("me -- tells you about yourself.")
    print("enter <building> -- go into a building")
    print("ship -- tells you about your ship")
    print("map <location or planets> -- shows the map of either your current location or the planets")
    print("inventory <me or ship> -- shows inventory of you or your ships cargo.")
    print("store <item name> -- moves item from your inventory into the ship's cargo.")
    print("retrieve <item name> -- moves item from the ship's cargo into your inventory")
    print("inspect <item> -- gives description of item")
    print("wait -- wait one second")
    print("wait <number> -- wait that many seconds.")
    print("whack <item> -- cuts down a tree")
    print("build house -- Costs 10 wood, builds a house")
    print("offer <someone> <something> -- offer item to another being")
    print("!! -- repeat last command.")
    print("? <command> -- learn more about command.")
    print()
    input("Press enter to continue...")

#Setup code above this line
#Game code below this line
    
def youvewon():
    clear()
    u = random.randint(1000,9000)
    input("You win!")
    input("You have rescued Jim!")
    input("Enjoy your travels; universe "+str(u)+" is forever in your debt!")




clear()
input("Checking for Save, press enter to continue.")
checkForSave()
lastCommand = None
playing = True
winner = False
while playing and player.alive:

    printSituation()
    commandSuccess = False
    timePasses = False
    while not commandSuccess:
    
        commandSuccess = True
        command = input("What now? ").lower()
        if command == "!!" and lastCommand != None:
            command = lastCommand
        elif command == "!!" and lastCommand == None:
            input("No previous commands.")
            command = ""
        commandWords = command.split()
        if command =="":
            print("Nothing Entered")
            commandSuccess = False 
            
        elif commandWords[0].lower() == "flyto":#goto the next planet. Checks the planets in the universe to see if the planet you want exists
            newWorld = None
            if not player.outside:
                input("This is not available from your current location.")
            else:
                for i in worlds:
                    if i.name.lower() == commandWords[1].lower():
                        newWorld = i
                if newWorld is None:
                    input("No such World")
                else:
                    if player.ship.canTravel(player.location.distanceTo(newWorld)):
                        player.ship.travelTo(newWorld,player.location.distanceTo(newWorld))
                        input("Press enter to fly to "+newWorld.name)
                    else:
                        print("Not enough fuel")
                        input("Press enter to continue.")
                    
                    
            timePasses = True
            
        elif commandWords[0].lower() == "pickup":
        #handles multi word objects and multiple pickups at once
        #checks for command pickup
        #targetName becomes the input minus pickup
        #findNameIn is the list of all inputs e.g. pickup wood 5 ['pickup','wood','5']
        #since the number will always end the input, we look at 0 to n-1 for the item name
        #if there is no number, then the target becomes the name
        #if there is a number, it combines all the words to create the item name
            targetName = command[7:].lower()
            findNameIn = targetName.split()
            n = len(findNameIn)-1
            hasNum = True
            target = ""
            if len(findNameIn)==1:
                target = targetName
            for i in range(n):
                target+=findNameIn[i]+" "
            target = target.rstrip()
            if target != "":
                number = 1
                try:
                    int(findNameIn[n])
                except ValueError:
                    hasNum = False
                if hasNum:
                    number = int(findNameIn[n])
                else:
                    if n>0:
                        target = target+" "+findNameIn[n].rstrip()
                i=0
                if player.location.items[target][0]>0:
                    while i<number and target and player.carriedWeight<player.carryCapacity:
                        targetItem = player.location.getItemByName(target)
                        if targetItem.name == "jim" and targetItem.satisfied == False:
                            input("Jim does not trust you.")
                            target = False
                        else:
                            player.pickup(targetItem)
                            if targetItem.name == "jim":
                                input("Bring our Jim home!")
                            i+=1
                else:
                    print("No such item.")
            else:
                print("No such item.")
                commandSuccess = False
                
        elif commandWords[0].lower() == "walkto":
        #walkto walks you to an on planet destination.
        #I think enter does the same thing but shh. we dont tell the player that.
            newLoc = None
            for i in player.location.locations:
                if i.name.lower() == commandWords[1].lower():
                    newLoc = i 
            if newLoc == None:
                print("No such World")
            else:
                player.location = newLoc
                input("Press enter to walk to "+newLoc.name)

            timePasses = True

                
        elif commandWords[0].lower() in ["inventory","inv"]:
            if len(commandWords)==1:
                player.showInventory() # if no inventory specified, default to your own
            elif commandWords[1].lower() == "me":
                player.showInventory()
            elif commandWords[1].lower()=="ship":
                player.ship.showInventory()
            else:
                input("Entity does not exist")#Inventory for random things wont work 
            
        elif commandWords[0].lower() == "help":
            showHelp()
            
        elif commandWords[0].lower() in ["exit","quit()","quit"]:#i kept typing quit instead of exit and got annoyed.
            playing = False
            
        elif commandWords[0] == "enter":
        #enter a building. checks for building on planet, if no such building, tells so.
        #effectively the same as walkto but more thematic to going inside a building. 
            buildingName = command[6:].lower()
            playerStart = player.location
            for i in player.location.locations:
                if i.name.lower() == buildingName:
                    i.enter(player)
                    player.outside = False
            if playerStart is player.location:
                input("No such location.")
                
            timePasses = True
            
            
        elif commandWords[0] == "build":#build object
            if commandWords[1] == "house" and player.location.type == "planet":
                player.location.buildHouse(player,updates)
            elif commandWords[1].lower() == "mill" and player.location.type == "river":
                player.location.buildMill(player,updates)
                
            timePasses = True
                
            
        elif commandWords[0] in ["whack"]:#whack object
            if commandWords[1] == "tree":
                if player.location.items["tree"][0]>0:
                    tree = player.location.getItemByName("tree")
                    player.exp+=tree.expGiven
                    tree.gather(player.holding)
                    
            timePasses = True
                        
        elif commandWords[0] == "refuel":#refuels ship with item
            player.ship.refuel(commandWords[1])
            
        elif commandWords[0] == "drop":# drop item from inventory
            player.drop(command[5:])
            
        elif commandWords[0].lower() == "inspect":#inspects item, prints its description
            targetName = command[8:]
            inspected = False
            itemList = player.location.items
            locationList = player.location.locations
            if targetName in itemList and itemList[targetName][0]>0:
                clear()
                print(itemList[targetName][1].desc)
                print()
                input("Press enter to continue...")
                inspected = True
            for i in locationList:
                if i.name == targetName:
                    clear()
                    print(i.desc)
                    print()
                    input("Press enter to continue...")

            
        elif commandWords[0].lower() == "map":#pulls up map of planet or current location. Needs maps for buildings implemented
            if len(commandWords)==1:
                input("No map specified. Press enter to contiue.")
            elif commandWords[1].lower() == "planets":
                map("planets")
            elif commandWords[1].lower()=="location":
                map(player.location)
            else:
                input("Map does not exist")
            
        elif commandWords[0].lower() == "me":#displays information about player 
            player.info()
            input("Press Enter to Contiue.")
            
        elif commandWords[0].lower() == "store":#place item from inventory into the ships cargo
            itemName = command[6:].lower() #all words after 'store'
            player.store(itemName)
            if itemName == "jim":
                youvewon()
                
        elif commandWords[0].lower() == "retrieve":#place item from the ship's cargo in inventory
            player.ship.retrieve(str(command[9:]).lower())
            
        elif commandWords[0].lower() == "ship":#view information about ship
            print("Current Fuel: "+str(player.ship.currentFuel))
            print("Fuel Capacity: "+str(player.ship.fuelCapacity))
            print("Fuel Efficieny: "+str(player.ship.fuelEfficieny))
            input("Press Enter to Contiue.")  

        elif commandWords[0] == "wait":#passes time for once or for x amount. 
            if len(commandWords) == 1:
                clear()
                time.sleep(1)                
                updater.updateAll()
            else:
                times = int(commandWords[1])
                clear()
                for i in range(times):
                    print(str(times-i))
                    time.sleep(1)
                    updater.updateAll()
        
        elif commandWords[0] == "leave":#if player is indoors, takes them outside. Otherwise does nothing.
            if player.location.type:
                player.location.leave(player)

                
        elif commandWords[0].lower() == "harvest":
        #used to gather electricity from mills. 
            if player.location.type == "mill":
                player.location.harvest()
            else:
                input("You are not at a mill.")
                
            timePasses = True
                
                
            
        elif commandWords[0].lower() == "attack":
            targetName = command[7:]
            target = player.location.getMonsterByName(targetName)
            
            if target != False:
                player.attackMonster(target)
            else:
                print("No such monster.")
                commandSuccess = False
               
        elif commandWords[0].lower() == "eat":
        #eat an item, if it isnt edible, then it will tell you it isnt edible.
        
            if commandWords[1] in player.items and player.items[commandWords[1]][0]>0:
                edible = player.items[commandWords[1]][len( player.items[commandWords[1]])-1]
                if edible.heals:
                    player.currentHealth+=edible.heals
                    player.remove(commandWords[1])
                else:
                    input("This is not edible.")
            else:
                input("You have none to eat.")
        elif commandWords[0] == "hold":
        #hold an item in inventory in your hand. 
            player.hold(commandWords[1])
            
        elif commandWords[0] == "make":
        #used to craft items
            if commandWords[1] == "axe":
                if player.items["wood"][0]>0:
                    newAxe = Axe.Axe(3,updates)
                    player.location.addItem(newAxe)
                    player.pickup(newAxe)
                    player.items["wood"][0]-=1
            timePasses = True

        elif commandWords[0].lower() == "offer":
            if commandWords[1].lower() == "jim":
                if commandWords[2].lower() == "red": # "vines" being word 3
                    if player.items["red vines"][0]>0:
                        if player.location.items["jim"][0]>0:
                            player.items["red vines"][0]-=1
                            Jim = player.location.getItemByName("jim")
                            Jim.satisfied = True
                            print()
                            input("Jim: Wow. That's so...thank you. You are too kind.")
                        else: 
                            input("Jim isn't here")
                    else: 
                        input("You don't have red vines")
                else:
                    print("Not a valid command")

                    
                    
        elif commandWords[0] == "save":
        #used to save
            save(currentos)
        else:
            print("Not a valid command")
            commandSuccess = False
            
        if command !="" and commandSuccess == True:
            lastCommand = command    
    if timePasses == True:
        updater.updateAll()
        


    


