from .item import Item
class Fuel(Item):
    #special item: has ability to fuel ship. List of possible fuels maintained in ships
    def __init__(self,name,description,updates):
        Item.__init__(self,name,description,1,updates)
        self.fuelAmount = 20