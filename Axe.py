from .item import Item
#from .Weapon import Weapon

class Axe(Item):
    
    def __init__(self,damage,updates):
        Item.__init__(self,"Axe","an axe",5,updates)
        self.damage = damage
        self.cost = 1