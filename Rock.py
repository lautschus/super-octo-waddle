from .item import Item
class Rock(Item): 
    def __init__(self,updates):
        Item.__init__(self,"Rock", "This is just a rock.",1,updates)
        self.id = 4