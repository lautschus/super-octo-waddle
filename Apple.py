from .item import Item
from .Food import Food
AppleID = 1
class Apple(Food):
    def __init__(self,updates):
        Food.__init__(self,"apple","An apple.",5,updates)