import random
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import updater

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    #Added name, weight, fuelAmount. 
    def __init__(self, name, desc, weight,updates):

        self.name = name.lower()
        self.desc = desc
        self.loc = None
        self.weight = weight
        self.updates = updates
        updates.append(self)
        
    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
        
    def putInRoom(self, room):
        self.loc = room
        room.addItem(self)
        
    def removeFromRoom(self,room):
        self.loc = room
        room.removeItem(self)
        
    def update(self):
        pass

        
        

                
        
        
        

        
    
