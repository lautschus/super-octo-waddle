import os
from items import *
import updater

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self,updates):
        self.type = "player"
        self.location = None
        self.level = 18
        self.items = {}
        self.currentHealth = 20
        self.maxHealth = 50*self.level
        self.alive = True
        self.ship = None
        self.carryCapacity = 20+10*self.level
        self.carriedWeight = 0
        self.outside = True
        self.exp = 20000
        self.holding = None
        self.updates = updates
        updates.append(self)
        
    def goDirection(self, direction):
        self.location = self.location.getDestination(direction)
        
    def pickup(self, item):
    #adds item to invetory dictionary
    #if item has never been seen, creates new entry
    #adds weight to amount carried
        if (self.carriedWeight+item.weight)>self.carryCapacity:
            print("You cannot carry anymore.")
            input("Press enter to continue.")
            return None
        if item.name in self.items:
            self.items[item.name][0]+=1
            self.items[item.name].append(item)
        else:
            self.items[item.name]=[1,item]
        item.loc = self
        self.carriedWeight+=item.weight
        self.location.removeItem(item)
        
    def drop(self,itemName):
    #removes 1 from item count and 1 instance from list
    #subtracts item weight from amount carried
    #puts object in current location
        if itemName in self.items:
            if self.items[itemName][0]>0:
                self.items[itemName][0]-=1
                item = self.items[itemName].pop()
                self.carriedWeight-=item.weight
                self.location.addItem(item)
        
    def remove(self,itemName):
    #removes item from inventory
    #subtracts weight
    #item goes poof
        if itemName in self.items:
            if self.items[itemName][0]>0:
                self.items[itemName][0]-=1
                listItem = self.items[itemName].pop()
                self.carriedWeight-=listItem.weight
                updater.deregister(listItem)
                
        
    def showInventory(self):
    #goes through dictionary
    #checks item name
    #checks item amount
    #prints item name x item amount
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i+" x "+str(self.items[i][0]))
        print()
        input("Press enter to continue...")
        
    def attackMonster(self, mon):
        clear()
        print("You are attacking " + mon.name)
        print()
        print("Your health is " + str(self.health) + ".")
        print(mon.name + "'s health is " + str(mon.health) + ".")
        print()
        if self.health > mon.health:
            self.health -= mon.health
            print("You win. Your health is now " + str(self.health) + ".")
            mon.die()
        else:
            print("You lose.")
            self.alive = False
        print()
        input("Press enter to continue...")
        
    def store(self,itemName):
    #move item from inventory to ship's cargo
        if itemName in self.items:
            if self.items[itemName][0] < 1:
                input("No "+itemName+"s "+"to store.")
            else:
                item = self.items[itemName].pop()
                self.carriedWeight -= item.weight
                self.ship.store(item)
                self.items[itemName][0]-=1
        else:
            return("What is a "+itemName+"?")

    def retrieve(self,itemname):
    #move item from ship's cargo to inventory
        self.ship.retrieve(itemname)


    def info(self):
    #prints information about self
        clear()
        print("Location: "+str(self.location.name))
        print("Health: " +str(self.currentHealth))
        print("Carried Weight: "+str(self.carriedWeight))
        if self.holding:
            print("Holding: "+self.holding.name)
        print("Level: "+str(self.level))
        print("Experience: "+str(self.exp))
        
    def update(self):
    
        if self.currentHealth<self.maxHealth:
            self.currentHealth+=1
            if self.exp >=50*self.level:
                self.exp-=50*self.level
                self.level+=1
                clear()
                input("You are now level "+str(self.level))
                
    def hold(self,itemName):
        if itemName in self.items:
            self.holding = self.items[itemName][len(self.items[itemName])-1]