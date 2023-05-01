#this class represents a player used in the Map

class Player:
    #a players label is equivelant to their name
    #troops available is how many troops they have available to deploy
    #territories are the territories they currently own
    def __init__(self, label, troopsAvailable=0):
        self.label = label
        self.troopsAvailable = troopsAvailable
        self.territories = set()
    
    def attack(self, fromTerritory, toTerritory):
        print("attacking")
    
    def __str__(self):
        return self.label