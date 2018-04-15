from .item import Item 

class RedVines(Item):
    def __init__(self,updates):
        Item.__init__(self,"red vines","The best the office of inclusive community has to offer.",0,updates)