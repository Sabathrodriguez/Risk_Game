#map class represents the gameplay map. Map takes in 2 players currently.
import sys
sys.path.insert(0,"../../")
from Models.Territory import Territory
sys.path.insert(0,"..")
from territories import Territories

class map:
    def __init__(self, players) -> None:
        self.players = players

        #init territories from generateTerritories method
        self.territories = self.generateTerritories()
        self.connectContinents()

    #get territories from Terroitories enum and return them as a list
    def generateTerritories(self):
        territories = {}
        for el in Territories:
            territories[el.value[0]] = Territory(el.value[0], el.value[1])

        return territories

    #connect all territories in all continents
    def connectContinents(self):
        self.connectNorthAmerica()

        self.connectSouthAmerica()

        self.connectAfrica()

        self.connectEurope()

        self.connectAsia()

        self.connectAustralia()

    #connect all territories in north america
    def connectNorthAmerica(self):
        self.connect('ALASKA', ['NORTH WESTERN TERRITORY', 'ALBERTA', 'KAMCHATKA'])            

        self.connect('NORTH WESTERN TERRITORY', ['ALASKA', 'ALBERTA', 'ONTARIO', 'GREENLAND'])

        self.connect('GREENLAND', ['NORTH WESTERN TERRITORY', 'ONTARIO', 'QUEBEC', 'ICELAND'])

        self.connect('ALBERTA', ['ALASKA', 'NORTH WESTERN TERRITORY', 'ONTARIO', 'WESTERN UNITED STATES'])
        
        self.connect('ONTARIO', ['NORTH WESTERN TERRITORY', 'WESTERN UNITED STATES', 'GREENLAND', 'ALBERTA', 'QUEBEC', 'EASTERN UNITED STATES'])

        self.connect('QUEBEC', ['GREENLAND', 'ONTARIO', 'EASTERN UNITED STATES'])

        self.connect('WESTERN UNITED STATES', ['ALBERTA', 'ONTARIO', 'EASTERN UNITED STATES', 'CENTRAL AMERICA'])

        self.connect('EASTERN UNITED STATES', ['QUEBEC', 'ONTARIO', 'WESTERN UNITED STATES', 'CENTRAL AMERICA'])

        self.connect('CENTRAL AMERICA', ['WESTERN UNITED STATES', 'EASTERN UNITED STATES'])
    
    #connect all territories in south america
    def connectSouthAmerica(self):
        self.connect('VENEZUELA', ['CENTRAL AMERICA', 'BRAZIL', 'PERU'])

        self.connect('PERU', ['VENEZUELA', 'BRAZIL', 'ARGENTINA'])

        self.connect('BRAZIL', ['VENEZUELA', 'PERU', 'ARGENTINA', 'NORTH AFRICA'])

        self.connect('ARGENTINA', ['PERU', 'BRAZIL'])
    
    #connect all territories in africa
    def connectAfrica(self):
        self.connect('NORTH AFRICA', ['BRAZIL', 'WESTERN EUROPE', 'SOUTHERN EUROPE', 'EGYPT', 'EAST AFRICA', 'CONGO'])

        self.connect('EGYPT', ['NORTH AFRICA', 'EAST AFRICA', 'SOUTHERN EUROPE', 'MIDDLE EAST'])

        self.connect('CONGO', ['NORTH AFRICA', 'EAST AFRICA', 'SOUTH AFRICA'])

        self.connect('EAST AFRICA', ['EGYPT', 'NORTH AFRICA', 'CONGO', 'SOUTH AFRICA', 'MADAGASCAR', 'MIDDLE EAST'])

        self.connect('SOUTH AFRICA', ['CONGO', 'EAST AFRICA', 'MADAGASCAR'])

        self.connect('MADAGASCAR', ['EAST AFRICA', 'SOUTH AFRICA'])

    #connect all territories in europe
    def connectEurope(self):
        self.connect('ICELAND', ['GREENLAND', 'GREAT BRITAIN', 'SCANDINAVIA'])
        
        self.connect('SCANDINAVIA', ['ICELAND', 'GREAT BRITAIN', 'NORTHERN EUROPE', 'UKRAINE'])

        self.connect('UKRAINE', ['SCANDINAVIA', 'URAL', 'NORTHERN EUROPE', 'AFGHANISTAN', 'MIDDLE EAST'])

        self.connect('GREAT BRITAIN', ['ICELAND', 'SCANDINAVIA', 'NORTHERN EUROPE', 'WESTERN EUROPE'])

        self.connect('NORTHERN EUROPE', ['WESTERN EUROPE', 'GREAT BRITAIN', 'SOUTHERN EUROPE', 'UKRAINE', 'SCANDINAVIA'])

        self.connect('WESTERN EUROPE', ['SOUTHERN EUROPE', 'GREAT BRITAIN', 'NORTHERN EUROPE', 'NORTH AFRICA'])

        self.connect('SOUTHERN EUROPE', ['WESTERN EUROPE', 'NORTH AFRICA', 'NORTHERN EUROPE', 'UKRAINE', 'EGYPT'])

    #connect all territories in asia
    def connectAsia(self):
        self.connect('SIBERIA', ['URAL', 'CHINA', 'MONGOLIA', 'IRKUTSK', 'YAKUTSK'])

        self.connect('YAKUTSK', ['SIBERIA', 'IRKUTSK', 'KAMCHATKA'])

        self.connect('IRKUTSK', ['SIBERIA', 'YAKUTSK', 'KAMCHATKA', 'MONGOLIA'])

        self.connect('KAMCHATKA', ['ALASKA', 'YAKUTSK', 'IRKUTSK', 'MONGOLIA', 'JAPAN'])

        self.connect('URAL', ['UKRAINE', 'SIBERIA', 'CHINA', 'AFGHANISTAN'])

        self.connect('MONGOLIA', ['SIBERIA', 'IRKUTSK', 'KAMCHATKA', 'JAPAN', 'CHINA'])

        self.connect('JAPAN', ['KAMCHATKA', 'MONGOLIA'])

        self.connect('AFGHANISTAN', ['URAL', 'UKRAINE', 'MIDDLE EAST', 'INDIA', 'CHINA'])

        self.connect('CHINA', ['SIBERIA', 'URAL', 'AFGHANISTAN', 'INDIA', 'SLAM', 'MONGOLIA'])

        self.connect('MIDDLE EAST', ['UKRAINE', 'AFGHANISTAN', 'INDIA', 'EAST AFRICA'])

        self.connect('INDIA', ['SLAM', 'CHINA', 'AFGHANISTAN', 'MIDDLE EAST'])

        self.connect('SLAM', ['INDIA', 'CHINA', 'INDONESIA'])

    #connect all territories in australia
    def connectAustralia(self):
        self.connect('INDONESIA', ['SLAM', 'NEW GUINEA', 'WESTERN AUSTRALIA'])

        self.connect('NEW GUINEA', ['INDONESIA', 'WESTERN AUSTRALIA', 'EASTERN AUSTRALIA'])

        self.connect('WESTERN AUSTRALIA', ['INDONESIA', 'NEW GUINEA', 'EASTERN AUSTRALIA'])

        self.connect('EASTERN AUSTRALIA', ['WESTERN AUSTRALIA', 'NEW GUINEA'])

    #connect fromTerritory to all territories in toTerritoryList
    def connect(self, fromTerritory, toTerritoryList):
        for el in toTerritoryList:
            self.territories[fromTerritory].adjacentTerritories.append(self.territories[el])
