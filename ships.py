import os
import updater

fuelList = ["wood","fuel","electricity"]
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
class Ship:
    def __init__(self,player,updates):
        self.fuelCapacity = 300
        self.currentFuel = self.fuelCapacity
        self.storageCapacity = 280
        self.currentStorage = 0#current weight held
        self.fuelEfficieny = 1
        self.takeOff = 10#fuel needed to initiate flight
        self.location = player.location#current location of the ship
        self.pilot = player#pilot of the ship
        self.cargo = {}#items stored in the ship
        updates.append(self)
    
    def update(self):
        pass
        
    def canTravel(self,distance):
    #checks if the ship can travel the distance with the amount of fuel it has.
        fuelToUse = distance/self.fuelEfficieny+self.takeOff
        newFuelLevel = self.currentFuel-fuelToUse
        if newFuelLevel<0:
            return False
        else:
            return True
            
    def travelTo(self,planet,distance):
    #travels to the given planet that is distance away
    # calculates/subtracts fuel
    #changes players location (the pilot of the ship)
        fuelToUse = distance/self.fuelEfficieny+self.takeOff
        newFuelLevel = self.currentFuel-fuelToUse
        self.currentFuel=newFuelLevel
        self.pilot.location = planet
    
    def store(self,item):
    # pass an item, if carrying too much, it will not allow to store.
    #if there is space, adds 1 to the item count and appends the item to the end of the list
    #if the item has never been in the inventory before, it creates a new spot in the dictionary keeping track of the cargo
        if (self.currentStorage+item.weight)>self.storageCapacity:
            print("Cannot store anymore.")
            input("Press enter to continue")
            return False
        else:
            if item.name in self.cargo:
                self.cargo[item.name][0]+=1
                self.cargo[item.name].append(item)
            else:
                self.cargo[item.name]=[1,item]
            self.currentStorage+=item.weight
    
    def retrieve(self,itemName):
    #take item from ships cargo and moves it to players inventory.
    #searches dictionary for item name, grabs the count
    #if count is 0, tells them they dont have enough of the item
    #if >0, adds subtracts 1 from cargo, pops the item from the end of cargo list
    #adds item instance to the end of inventory list
        itemName = itemName.lower()
        if itemName in self.cargo: 
            if self.cargo[itemName][0]>0:
                self.pilot.items[itemName][0]+=1
                self.cargo[itemName][0]-=1
                self.pilot.items[itemName].append(self.cargo[itemName].pop())
        else:
            input("Not enough of "+itemName)
                
    def remove(self,itemName):
    #removes item from cargo if there is 1 or more
    #removes count/instance of item from cargo list
        if itemName in self.cargo:
            if self.cargo[itemName][0]>0:
                item = self.cargo[itemName].pop()
                self.cargo[itemName][0]-=1
                self.currentStorage-=item.weight
                updater.deregister(item)
            
            
    def showInventory(self):
    #goes through the dictionary of cargo
    #checks count cargo[0]
    #prints name x count
        clear()
        print("Your ships cargo:")
        print()
        for i in self.cargo:
            print(i+" x "+str(self.cargo[i][0]))
        print()
        input("Press enter to continue...")
        
    def refuel(self,itemName):
    #asks how many of x item you would like to use to refuel
    #checks if item is a possible fuel with fuel list
    #checks the ship inventory and player inventory for the fuel starting with the ship inventory
    #if there is enough to use it keeps going
    #if there isnt enough, it stops refueling and tells that you ran out
        times = int(input("How many "+itemName+" would you like to use? "))  
        itemName = itemName.lower()
        if itemName in fuelList and self.currentFuel < self.fuelCapacity:
            for i in range(times):   
                if itemName in self.cargo or itemName in self.pilot.items:
                    if itemName in self.cargo and self.cargo[itemName][0]>0:
                        self.currentFuel+=self.cargo[itemName][1].fuelAmount
                        self.remove(itemName)
                    elif itemName in self.pilot.items and self.pilot.items[itemName][0]>0:
                        self.pilot.store(itemName)
                        self.currentFuel+=self.cargo[itemName][1].fuelAmount
                        self.remove(itemName)
                    else:
                        input("No more "+itemName+" to use.")
                        return None
        elif self.currentFuel >= self.fuelCapacity:
            input("Your fuel is full.")
        else:
            input(itemName+" cannot be used as fuel.")
                    
            
            
        
        