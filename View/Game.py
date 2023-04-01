from tkinter import *
import tkinter.font as font
import sys
sys.path.insert(0,"..")
from Models.Map import map
from Models.Player import Player
from functools import partial
import random

class Game:
    
    def __init__(self):
        self.player1 = Player('Player 1', 15)
        self.player2 = Player('Player 2', 0)

        self.players = [self.player1, self.player2]

        self.currentPlayer = self.players[0]

        self.root = Tk()

        self.root.geometry('1440x1080')

        self.canvas = Canvas(self.root, width=1440, height=1080)

        self.myFont = font.Font(size=8)

        self.map = map(self.players)

        self.buttonMap = {}
        
        self.labelMap = {}

        self.x, self.y = -140, 0

        self.i = 0

        self.phase = 'deploy'
        
        self.turns = 2

        self.attacked = False

        self.deployed = False

        self.attackingTerritory = None

        self.attackedTerritory = None

        self.enemy = self.players[1]      

        self.isDoneAttackingPressed = False  

    def open_popup(self, text):
        top= Toplevel(self.root)
        top.geometry("250x750")
        top.title("phase")
        Label(top, text= text, font=('Mistral 18 bold')).place(x=150,y=80)

    def selectTerritory(self, territory):    
        
        availableTerritoriesToAttack = []
        playerOwnedTerritoriesList = []
        
        #player 1
        if self.currentPlayer == self.players[0]:
            if self.phase == 'deploy':
                #cannot change to attack phase until all troops have been deployed
                self.deployPhase(territory)
            elif self.phase == 'attack': 
                #iterate through territories player owns
                self.attackPhase(self.currentPlayer, playerOwnedTerritoriesList, availableTerritoriesToAttack, territory)

        #player 2
        else:
            if self.phase == 'deploy':
                #cannot change to attack phase until all troops have been deployed
                self.deployPhase(territory)
            elif self.phase == 'attack': 
                #iterate through territories player owns and append territories that they're able to attack
                self.attackPhase(self.currentPlayer, playerOwnedTerritoriesList, availableTerritoriesToAttack, territory)

    def isDoneAttacking(self):

        self.phase = 'deploy'                

        self.attacked = True
        self.isDoneAttackingPressed = False
        
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
            self.enemy = self.player1
        else:
            self.currentPlayer = self.player1
            self.enemy = self.player2
        self.deployed = False
        self.attackedTerritory = None
        self.attackingTerritory = None
        self.isDoneAttackingPressed = True        

        if self.turns > 0:
            self.currentPlayer.troopsAvailable += 15
        self.turns += 1
    
    def startGame(self):                  

        #turn map into list of keys and values
        territoryList = list(self.map.territories.items())

        #initial number of armies to spread
        player1Armies = 40
        player2Armies = 40

        #alternate between players
        flag = False

        #randomly initialize armies in territories
        for i in range(len(territoryList)):
            randomTerritory = territoryList.pop(random.randrange(len(territoryList)))
            if flag:
                randomNumArmies1 = random.randint(0, player1Armies)
                player1Armies -= randomNumArmies1
                if player1Armies > 0 and randomNumArmies1 > 0:
                    self.map.territories[randomTerritory[0]].numberOfTroops = randomNumArmies1
                    self.map.territories[randomTerritory[0]].player = self.player1.label
                flag = False
            else:
                randomNumArmies2 = random.randint(0, player2Armies)
                player2Armies -= randomNumArmies2
                if player2Armies > 0 and randomNumArmies2 > 0:
                    self.map.territories[randomTerritory[0]].numberOfTroops = randomNumArmies2
                    self.map.territories[randomTerritory[0]].player = self.player2.label
                flag = True        

        #sort territories in map
        myKeys = list(self.map.territories.keys())
        myKeys.sort()
        sorted_dict = {i: self.map.territories[i] for i in myKeys}
        self.map.territories = sorted_dict

        #initialize territories        
        for k, v in self.map.territories.items():
            h = 2
            w = 18
            z = 50
            t = 20 
            a = 20
            b = 20
            c = 20
            d = 20
            e = 20
            f = 20
            if k == 'ALASKA':
                self.x = 0
                self.y = 0
                w = 6
            elif k == 'NORTH WESTERN TERRITORY':
                self.x = 80 + f
                self.y = 0
                #alaska to north western territory
                self.canvas.create_line(10, 10, 80 + f, 10, width=2)
            elif k == 'GREENLAND':
                self.x = 230 + 2*f
                self.y = 0
                w = 8
                #north western tetrritory to greenland
                self.canvas.create_line(80 + f, 10, 230 + 2*f, 10, width=2)
            elif k == 'ICELAND':
                self.x = 420 + 3*f
                self.y = 0
                w = 6
                #greenland to iceland
                self.canvas.create_line(230 + 2*f, 10, 420 + 3*f, 10, width=2)
            elif k == 'SCANDINAVIA':
                self.x = 500 + 4*f
                self.y = 0
                w = 10
            elif k == 'SIBERIA':
                self.x = 840 + 5*f
                self.y = 0
                w = 6
            elif k == 'YAKUTSK':
                self.x = 930 + 6*f
                self.y = 0
                w = 6
            elif k == 'KAMCHATKA':
                self.x = 1010 + 7*f
                self.y = 0
                w = 8
            #-----------------------------#
            elif k == 'ALBERTA':
                self.x = 0
                self.y = 30 + t
                w = 6
                #alaska to alberta
                self.canvas.create_line(10, 10, 10, 30 + t, width=2)
                #north western territory to alberta
                self.canvas.create_line(80 + f, 10, 50, 30 + t, width=2)
            elif k == 'ONTARIO':
                self.x = 80 + f
                self.y = 30 + t
                w = 6
                #north western territory to ontario
                self.canvas.create_line(100 + f, 10, 100 + f, 30 + t, width=2)
                #greenland to ontario                
                self.canvas.create_line(230 + 2*f, 10, 100 + f, 30 + t, width=2, fill='red')
            elif k == 'QUEBEC':
                self.x = 160 + 2*f
                self.y = 30 + t
                w = 6
                #greenland to quebec
                self.canvas.create_line(230 + 2*f, 10, 190 + 2*f, 30 + t, width=2)
            elif k == 'GREAT BRITAIN':
                self.x = 420 + 3*f
                self.y = 30 + t
                w = 10
            elif k == 'NORTHERN EUROPE':
                self.x = 520 + 4*f
                self.y = 30 + t
                w = 14
            elif k == 'UKRAINE':
                self.x = 650 + 5*f
                self.y = 30 + t
                w = 6
            elif k == 'URAL':
                self.x = 840 + 6*f
                self.y = 30 + t
                w = 4
            elif k == 'IRKUTSK':
                self.x = 910 + 7*f
                self.y = 30 + t
                w = 8
            elif k == 'MONGOLIA':
                self.x = 1000 + 8*f
                self.y = 30 + t
                w = 8
            elif k == 'JAPAN':
                self.x = 1090 + 9*f
                self.y = 30 + t
                w = 6
            #-----------------------------#
            elif k == 'WESTERN UNITED STATES':
                self.x = 0
                self.y = 60 + t + a

            elif k == 'EASTERN UNITED STATES':
                self.x = 140 + f
                self.y = 60 + t + a
            elif k == 'WESTERN EUROPE':
                self.x = 420 + 2*f
                self.y = 60 + t + a
                w = 12
            elif k == 'SOUTHERN EUROPE':
                self.x = 540 + 3*f
                self.y = 60 + t + a
                w = 12
            elif k == 'AFGHANISTAN':
                self.x = 840 + 4*f
                self.y = 60 + t + a
                w = 8
            elif k == 'CHINA':
                self.x = 940 + 5*f
                self.y = 60 + t + a
                w = 4
            #-----------------------------#
            elif k == 'CENTRAL AMERICA':
                self.x = 0 
                self.y = 90 + t + a + b
                w = 12
                self.canvas.create_line(10, 90 + t + a + b, 10, 120 + z + t + a + b, width=2)
                self.canvas.pack()
            elif k == 'MIDDLE EAST':
                self.x = 840 + f
                self.y = 90 + t + a + b
                w = 8
            elif k == 'INDIA':
                self.x = 930 + 2*f
                self.y = 90 + t + a + b
                w = 4
            elif k == 'SLAM':
                self.x = 1000 + 3*f
                self.y = 90 + t + a + b
                w = 4            
            #-----------------------------#            
            elif k == 'VENEZUELA':
                self.x = 0
                self.y = 120 + z + t + a + b
                w = 8
            elif k == 'NORTH AFRICA':
                self.x = 540 + f
                self.y = 120 + z + t + a + b
                #brazil to north africa
                self.canvas.create_line(150, 150 + z + t + a + b + c, 540 + f, 130 + z + t + a + b, width=2)
                w = 10
            elif k == 'EGYPT':
                self.x = 640 + 2*f
                self.y = 120 + z + t + a + b
                w = 6
            elif k == 'INDONESIA':
                self.x = 930 + 3*f
                self.y = 120 + z + t + a + b
                w = 10
            elif k == 'NEW GUINEA':
                self.x = 1100 + 4*f
                self.y = 120 + z + t + a + b
                w = 10
            #-----------------------------#
            elif k == 'BRAZIL':
                self.x = 100
                self.y = 150 + z + t + a + b + c
                w = 6
                self.canvas.create_line(0, 120 + z + t + a + b, 100, 150 + z + t + a + b + c, width=2)
            elif k == 'CONGO':
                self.x = 540 + f
                self.y = 150 + z + t + a + b + c
                w = 4
            elif k == 'EAST AFRICA':
                self.x = 640 + 2*f
                self.y = 150 + z + t + a + b + c
                w = 8
            elif k == 'WESTERN AUSTRALIA':
                self.x = 930 + 3*f
                self.y = 150 + z + t + a + b + c
                w = 16
            elif k == 'EASTERN AUSTRALIA':
                self.x = 1100 + 4*f
                self.y = 150 + z + t + a + b + c
                w = 16
            #-----------------------------#
            elif k == 'PERU':
                self.x = 0
                self.y = 180 + z + t + a + b + c + d
                w = 4
                #venezuela to peru
                self.canvas.create_line(10, 120 + z + t + a + b, 10, 180 + z + t + a + b + c + d, width=2)
                #brazil to peru
                self.canvas.create_line(100, 150 + z + t + a + b + c, 10, 180 + z + t + a + b + c + d, width=2)
            elif k == 'SOUTH AFRICA':
                self.x = 540 + f
                self.y = 180 + z + t + a + b + c + d
                w = 10
            elif k == 'MADAGASCAR':
                self.x = 640 + 2*f
                self.y = 180 + z + t + a + b + c + d
                w = 8
            #-----------------------------#
            elif k == 'ARGENTINA':
                self.x = 0
                self.y = 210 + z + t + a + b + c + d + e
                w = 8    
                #peru to argentina
                self.canvas.create_line(10, 180 + z + t + a + b + c + d, 10, 210 + z + t + a + b + c + d + e, width=2)
                #brazil to argentina
                self.canvas.create_line(100, 150 + z + t + a + b + c, 60, 210 + z + t + a + b + c + d + e, width=2)

            self.i += 1
            t = Button(self.root, text = str(k) + " " + str(self.map.territories[k].numberOfTroops) + '\n' + (self.map.territories[k].player if self.map.territories[k].player is not None else ''), height=h, width=w, bd = '2', command = partial(self.selectTerritory, k))
            t.place(x=self.x, y=self.y)
            t['font'] = self.myFont
            self.buttonMap[k] = t        

        #initialize buttons
        isDoneAttacking = Button(self.root, text='press if done attacking', height=2, width= 18, command=(self.isDoneAttacking))
        isDoneAttacking.place(x=100, y=500)
        self.buttonMap['isDoneAttacking'] = isDoneAttacking

        attackingTerritoryLabel = Label(self.root, text='attacking terrritory: ')
        attackingTerritoryLabel.place(x=1080/2, y=450)
        self.labelMap['attackingTerritoryLabel'] = attackingTerritoryLabel

        attackedTerritoryLabel = Label(self.root, text='territory being attacked: ')
        attackedTerritoryLabel.place(x=1080/2, y=550)
        self.labelMap['attackedTerritoryLabel'] = attackedTerritoryLabel

        self.root.mainloop()

    def nextPhase(self):

        if self.attacked == False:
            self.buttonMap['phaseButton'].configure(text= 'Attack Phase')

        self.deployed = True
        self.attackedTerritory = None
        self.attackingTerritory = None

    def attackPhase(self, player, playerOwnedTerritoriesList, adjacentTerritories, territory):
        playerOwnedTerritories = ''
        #iterate through all territories in map
        for k, v in self.map.territories.items():
            if self.map.territories[k].player == self.currentPlayer.label:
                playerOwnedTerritories += k  + ' -> '
                playerOwnedTerritoriesList.append(k)
                #iterate through all territories adjacent to k
                for t in self.map.territories[k].adjacentTerritories:
                    if self.map.territories[t.label].player is not self.currentPlayer.label:                            
                        adjacentTerritories.append(t.label)
                    else:
                        playerOwnedTerritories += t.label + ', '
                playerOwnedTerritories += '\n'      

        
        if self.attackingTerritory is not None:                               
            self.labelMap['attackingTerritoryLabel'].configure(text='attacking territory: ' + str(self.attackingTerritory))                         
            if self.attackedTerritory is not None:        
                self.labelMap['attackedTerritoryLabel'].configure(text='territory being attacked: ' + str(self.attackedTerritory))
                #check if current player has more troops than enemy player, if so, adjust territory accordingly
                if self.attackingTerritory.numberOfTroops > self.attackedTerritory.numberOfTroops and self.map.territories[territory].player is not self.currentPlayer.label:
                    self.attackedTerritory.numberOfTroops = 1
                    self.buttonMap[territory].configure(text= territory + " " + str(1)+ '\n' + self.currentPlayer.label)   
                    self.attackingTerritory.numberOfTroops -= 1
                    self.attackedTerritory.player = self.currentPlayer
                    self.attackingTerritory = None
                    self.attackedTerritory = None
                    
                    #add territory to players territory list and remove from opponents
                    if self.currentPlayer == self.player1:
                        self.player1.territories.append(territory)
                        index = self.player2.territories.index(territory)
                        self.player2.territories.pop(index)  
                    else:
                        self.player2.territories.append(territory)
                        index = self.player1.territories.index(territory)                              
                        self.player1.territories.pop(index)
                    
            else: 
                #we need to make sure that the territory being chosen to be attacked
                #isn't owned by the same player or empty.
                if self.map.territories[territory].label in adjacentTerritories:
                    canAdd = True
                    #iterate through all territories player1 owns
                    #and if they already own the property dont attack  
                    
                    #player1
                    if self.currentPlayer == self.player1:                      
                        for t in self.player1.territories:
                            if territory == t:
                                canAdd = False
                                break
                    #player2
                    else:                      
                        for t in self.player2.territories:
                            if territory == t:
                                canAdd = False
                                break

                    #check if territory is empty, if it is then we can't attack
                    #otherwise, we can
                    if self.map.territories[territory].player is None:
                        canAdd = False
                    
                    if canAdd == True:
                        self.attackedTerritory = self.map.territories[territory]

        else:
            #if territory clicked is a territory that the current player owns, then we can attack from it
            if self.map.territories[territory].label in playerOwnedTerritoriesList:
                self.attackingTerritory = self.map.territories[territory]

    def deployPhase(self, territory):
        if self.currentPlayer.troopsAvailable == 0 or self.deployed == True:
            self.phase = 'attack'
            self.attacked = False

        else:
            if self.map.territories[territory].player is None or self.currentPlayer.label == self.map.territories[territory].player:
                self.currentPlayer.troopsAvailable -= 1
                self.map.territories[territory].numberOfTroops += 1
                self.map.territories[territory].player = self.currentPlayer.label
                self.currentPlayer.territories.append(territory)
                self.buttonMap[territory].configure(text= territory + " " + str(self.map.territories[territory].numberOfTroops)+ '\n' +self.map.territories[territory].player)

newGame = Game()
newGame.startGame()