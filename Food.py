from .item import Item
import random
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import updater
class Food(Item):

    def __init__(self,name,description,heals,updates):
        Item.__init__(self,name,description,1,updates)
        self.heals = heals
        self.decayTime = random.randint(3,10)
        self.timeAlive= 0
        
    def update(self):
        if self.loc.type != "player":
            self.timeAlive+=1
            if self.timeAlive>self.decayTime:
                self.loc.removeItem(self)
                updater.deregister(self)
                
    def setHeal(self, n):
        self.heals = n
        
