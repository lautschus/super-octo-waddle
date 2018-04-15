from .item import Item
import random
import time
from .generate import Generate

class Resource(Item):
    def __init__(self,name,description,weight,updates):
        Item.__init__(self,name,description, weight,updates)
        self.expGiven = 0
        self.durability = 0
        self.drops = {}
        self.dropN = 0

    def gather(self,item):
        if item and item.damage and item.damage > 0:
            damage = item.damage
        else:
            damage = 1
        numberOfHits = self.durability//damage
        while numberOfHits > 0:
            print("Dink..")
            time.sleep(.6)
            numberOfHits-=1
        dropN = random.randint(1,5)
        for i in range(dropN):
            for i in self.drops:
                if random.random()<self.drops[i]:
                    Generate(i,self.loc)
        

    def addDrop(self,id,probability):
        self.drops[id] = probability

    def setDurability(self, d):
        self.durability = d
        
    def setExp(self, exp):
        self.expGiven = exp
            
    