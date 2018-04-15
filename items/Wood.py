from .item import Item
class Wood(Item):
    #wood, comes from trees. Used to build things, horrible fuel. But a wood fueled spaceship is logical right?
    def __init__(self,updates):
        Item.__init__(self,"Wood","Good for building, maybe burning?",2,updates)
        self.fuelAmount = .1