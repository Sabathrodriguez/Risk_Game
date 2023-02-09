#map class represents the gameplay map. Map takes in 2 players currently.
import sys
sys.path.insert(0,"..")
from territories import Territories
from Territory import Territory

class map:
    def __init__(self, players) -> None:
        self.players = players

        #init territories from generateTerritories method
        self.territories = self.generateTerritories()
        self.connectTerritories()

    #get territories from Terroitories enum and return them as a list
    def generateTerritories(self):
        territories = {}
        for el in Territories:
            territories[el.value[0]] = Territory(el.value[0], el.value[1])

        return territories

    def connectTerritories(self):
        self.connect('ALASKA', ['NORTH WESTERN TERRITORY', 'ALBERTA', 'KAMCHATKA'])            

        self.connect('NORTH WESTERN TERRITORY', ['ALASKA', 'ALBERTA', 'ONTARIO', 'GREENLAND'])

        self.connect('GREENLAND', ['NORTH WESTERN TERRITORY', 'ONTARIO', 'QUEBEC', 'ICELAND'])

        self.connect('ALBERTA', ['ALASKA', 'NORTH WESTERN TERRITORY', 'ONTARIO', 'WESTERN UNITED STATES'])
        
        self.connect('ONTARIO', ['NORTH WESTERN TERRITORY', 'WESTERN UNITED STATES', 'GREENLAND', 'ALBERTA', 'QUEBEC', 'EASTERN UNITED STATES'])

        self.connect('QUEBEC', ['GREENLAND', 'ONTARIO', 'EASTERN UNITED STATES'])
        

    def connect(self, fromTerritory, toTerritoryList):
        for el in toTerritoryList:
            self.territories[fromTerritory].adjacentTerritories.append(self.territories[el])


mp = map(['bob'])
for k in mp.territories.keys():    
    if len(mp.territories[k].adjacentTerritories) > 0:
        print(k, end='->')
        for v in mp.territories[k].adjacentTerritories:
            print(v, end=", ")
        print()