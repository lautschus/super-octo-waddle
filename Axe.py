from .item import Item
#from .Weapon import Weapon
class Axe(Item):
    def __init__(self,updates,player):
        Item.__init__(self,"Axe","an axe",5,updates)
        self.damage = 1.4
        self.cost = 1
        self.level = 1
        self.id = 2
        self.expGiven = 10
        player.exp+=5
        player.location.addItem(self)
        player.remove("wood",1)
        
    def upgrade(self):
        player = self.loc
        level = self.level
        if player.type == "player":
            if self.level == 1:
                if player.items["wood"][0]>0:
                    player.remove("wood",1)
                    self.damage+=.2
                    self.level+=1
                    self.name = "axe+1"
                    player.popItem("axe")
                    player.addItem(self)
                    player.exp+=self.expGiven
                    self.desc = "An axe, but a wee bit better."
                else:
                    input("You need 1 wood to upgrade.")
                    
            elif self.level == 2:
                if player.items["wood"][0]>0 and "rock" in player.items and player.items["rock"][0]>1:
                    player.remove("wood",1)
                    player.remove("rock",2)
                    self.damage+=.4
                    self.level+=1
                    self.name = "axe+2"
                    player.popItem("axe+1")
                    player.addItem(self)
                    player.exp+=self.expGiven*2
                else:
                    input("You need 1 wood and 2 rocks to upgrade.")
                    
            elif self.level == 3:
                if (
                player.items["wood"][0]>0 
                and "rock" in player.items 
                ):
                    player.remove("wood",3)
                    player.remove("rock",5)
                    self.damage+=.4
                    self.level+=1
                    self.name = "axe+3"
                    player.popItem("axe+2")
                    player.addItem(self)
                    player.exp+=self.expGiven*4
                else:
                    input("You need 3 wood and 5 rocks to upgrade.")               
            
            
        