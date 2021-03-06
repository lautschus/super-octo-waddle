from .item import Item
import random
from .Wood import Wood
from .Food import Food

class Tree(Item):
    #tree, can chop down. drops between 1-5 wood. weighs a lot.
    def __init__(self,updates):
        Item.__init__(self,"tree","1 tallboi",3000,updates)
        self.expGiven = 5
        self.durability = 10
        
    def gather(self,item):
        if item:
            damage = item.damage
        else:
            damage = 1
        numberOfHits = random.randint(1,self.durability//damage)

        while numberOfHits>0:
            input("Dink..")
            numberOfHits-=1
        badAppleProb = .1
        woodNum = random.randint(1,3)
        for i in range(woodNum):
            self.loc.addItem(Wood(self.updates))
        self.removeFromRoom(self.loc)
        appleNum = random.randint(0,2)
        if random.random()<=badAppleProb:
            self.loc.addItem(Food("bad apple","A bad apple.",-5,self.updates))
        for i in range(appleNum):
            self.loc.addItem(Food("apple","An apple.",5,self.updates))