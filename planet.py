import random
from room import Room
from items.item import Item
from items import Fuel

class Key(Item):
    #used to unlock buildings. key info kept track of by house. Name of key corresponds to houses name
    #if the house name is changed, the key name will be changed
    #dont drop the key.
    def __init__(self,House,updates):
        Item.__init__(self,House.name.lower()+" key", "might unlock something?",.1,updates)
        

class House(Room):
    #special room: only connects to planet
    #has rooms 3 rooms by default
    #with a house comes a key, key is added to creator inventory.
    #key is assigned to house on creation
    def __init__(self,name,description,player,updates):
        Room.__init__(self,description,updates)
        self.name = name.lower()
        self.cost = 10
        self.key = Key(self,updates)
        self.hasLock = True
        self.Locked = True
        self.type = "house"
        self.discoveredPlanets = []
        self.onPlanet = player.location
        self.size = [10,10]

        
    def setName(self,name):
    #rename the house, renames the key. 
        self.name = name.lower()
        self.key.name = name+" key"
    
    def setDescription(self,description):
    #used to change description of the house
        self.desc = description
        
    def enter(self,player):
    #checks if the house is locked
    #if house is locked, checks if player entering has the key
    #if they do, unlock door and move person inside
    #if door is not locked, person enters
        if self.Locked:
            if self.key.name in player.items:
                if player.items[self.key.name][0]>=1:
                    self.unlock()
                    player.location = self
                else:
                    input("You do not have the key to this door.")
            else:
                input("You do not have the key to this door.")
        else:
            player.location = self
            
    def createRoom(self,name,updates):
    #creates a new room with name <name> and generic description
        newRoom = Room("a cozy room",updates)
        self.locations.append(newRoom)
        newRoom.name = name
        
    def leave(self,player):
    #leaves house, asks if you would like to lock the door on your way out.
    #dont leave the key inside.
    #moves player to the planet the building is on
        decision = input("Would you like to lock the door? yes/no ")
        if decision.lower() == "yes":
            self.lock()
        player.location = self.onPlanet
        
    def lock(self):
    #lock house
        self.Locked = True
        
    def unlock(self):
    #unlock house
        self.Locked = False
    
class Planet(Room):
    def __init__(self,name,description,distanceFromCenter,updates):
    #Basically big rooms, just called planets with a few extra details.
        Room.__init__(self,description,updates)   
        self.x = random.choice([-1,1])*random.random()*distanceFromCenter**.5
        self.y = random.choice([-1,1])*((distanceFromCenter**2-(self.x)**2))**.5
        self.type = "planet"
        self.name = name
        
    def distanceTo(self,planet):
    #calculates the distance another planet
        distance =  ((planet.x-self.x)**2+(planet.y-self.y)**2)**.5
        return distance
        
    def buildHouse(self,player,updates):
    #add a house to the planet
    #creates a new house with living room, bedroom, kitchen
    #places key in players inventory
    #removes cost of house worth of wood from players inventory
    #asks for player to name/describe house
    #if not enough wood, does not build house.
        newHouse = House("","",player,updates)
        if "wood" not in player.items:
            input("No wood.")
            return None
        if player.items["wood"][0]>=newHouse.cost:
            newHouse.setName(input("What would you like to name your house? ").lower())
            newHouse.setDescription(input("How would you describe your house? "))
            self.addLocation(newHouse)
            newHouse.createRoom("Bedroom",updates)
            newHouse.createRoom("Living Room",updates)
            newHouse.createRoom("Kitchen",updates)
            player.items[newHouse.key.name]=[1, newHouse.key]
            player.remove("wood",newHouse.cost)
        else:
            input("You do not have enough wood.")
            
        
        
        
class River(Room):

    def __init__(self,planet,updates):
        Room.__init__(self,'Home of fishes. Welcome.',updates)
        #self.name = name
        self.onPlanet = planet
        self.name = 'river'
        self.type = 'river'

    def harness(self):
        if len(self.locations) == 2:
            print('This river cannot generate more energy than it does currently.')
        else:
            buildMill(self,river)

    def buildMill(self,player,updates):
        newMill = Mill(player.location,updates)
        if "wood" not in player.items:
            input("No wood.")
            return None
        if player.items["wood"][0]>=newMill.cost:
            self.locations.append(newMill)
            player.remove("wood",newMill.cost)
        else:
            input("You do not have enough wood.")

    def leave(self,player):
        player.location = self.onPlanet


class Mill(Room):

    def __init__(self, river, updates):
        Room.__init__(self,'mill: generates 1 fuel per second',updates)
        self.time = 0
        self.generated = 0
        self.fuelCap = 5
        self.type = "mill"
        self.cost = 5
        self.name = 'Mill' + str(len(river.locations)+1)
        self.river = river

    def enter(self,player):
        player.location = self

    def leave(self, player):
        player.location = self.river

    def update(self):
        self.time += 1
        input(["time",self.time])
        if self.generated < self.fuelCap and self.time>=10:
            self.time-=10
            input("fuel generated")
            self.generated += 1

    def harvest(self):
        for i in range(self.generated):
            self.addItem(Fuel.Fuel('electricity','Pure mechanical agency. Fills 1 fuel.',self.updates))
        self.generated = 0 

    