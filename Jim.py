from .item import Item

class Jim(Item):

    def __init__(self,updates):
        Item.__init__(self,"Jim","An unstoppable intellectual juggernaut. Extremely powerful.",180,updates)
        self.satisfied = False 