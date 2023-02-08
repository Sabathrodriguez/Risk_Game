#map class represents the gameplay map. Map takes in 2 players currently.
import sys
sys.path.insert(0,"..")
from territories import Territories

class map:
    def __init__(self, players) -> None:
        self.players = players

        #init territories from generateTerritories method
        self.territories = self.generateTerritories()

    #get territories from Terroitories enum and return them as a list
    def generateTerritories(self):
        territories = []
        for el in Territories:
            territories.append(el.value)
            
        return territories


mp = map(['bob'])
print(mp.territories)