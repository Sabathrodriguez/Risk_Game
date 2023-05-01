#this class represents a single territory in the Map

class Territory:
    #label represents a territories name
    #continent represents what continent a territory is in
    def __init__(self, label, continent):
        self.label = label
        self.player = None
        self.numberOfTroops = 0
        self.adjacentTerritories = []
        self.continent = continent
        self.selected = False
        
    def __str__(self) -> str:
        return self.label + ": " + self.continent