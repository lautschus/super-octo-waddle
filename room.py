import random

class Room:
    def __init__(self, description,updates):
        self.name = None
        self.type = "room"
        self.desc = description
        self.monsters = []
        self.exits = []
        self.items = {}
        self.updates = updates
        self.hasLock = False
        self.Locked = False
        updates.append(self)
        self.locations = []

    def addExit(self, exitName, destination):
        self.exits.append([exitName, destination])
    def getDestination(self, direction):
        for e in self.exits:
            if e[0] == direction:
                return e[1]
    def connectRooms(room1, dir1, room2, dir2):
        #creates "dir1" exit from room1 to room2 and vice versa
        room1.addExit(dir1, room2)
        room2.addExit(dir2, room1)
    def exitNames(self):
        return [x[0] for x in self.exits]
    def addItem(self, item):
        if item.name in self.items:
            self.items[item.name][0]+=1
            self.items[item.name].append(item)
        else:
            self.items[item.name]=[1,item]
        item.loc = self

    def removeItem(self, item):
        self.items[item.name][0]-=1
        self.items[item.name].pop()
    def addMonster(self, monster):
        self.monsters.append(monster)
    def removeMonster(self, monster):
        self.monsters.remove(monster)
    def hasItems(self):
        return self.items != {}
    def getItemByName(self, name):
        for i in self.items:
            if i.lower() == name.lower():
                return self.items[i][len(self.items[i])-1]
        return False
    def hasMonsters(self):
        return self.monsters != []
    def getMonsterByName(self, name):
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
        return False
    def randomNeighbor(self):
        return random.choice(self.exits)[1]
        
    def enter(self,player):#moves player into room
        player.location = self

    def update(self):
        pass
        
    def addLocation(self,location):
        self.locations.append(location)