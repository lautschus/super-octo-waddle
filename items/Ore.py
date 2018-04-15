from .item import Item
from .rock import Rock

class Ore(Item):
    def __init__(self, updates):
        Item.__init__(self,updates,"Ore.", "A bit shiny?",500,updates)
        self.durability = 20
        
    def mine(self):
        hits = None