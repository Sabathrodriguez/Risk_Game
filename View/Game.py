from tkinter import *
import tkinter.font as font
import sys
sys.path.insert(0,"..")
from Models.Map import map
from Models.Player import Player
from functools import partial

class Game:
    
    def __init__(self):
        self.player1 = Player('Player 1', 40)
        self.player2 = Player('Player 2', 40)

        self.players = [self.player1, self.player2]

        self.currentPlayer = self.players[0]

        self.root = Tk()

        self.root.geometry('1080x1080')

        self.myFont = font.Font(size=8)

        self.map = map(self.players)

        self.buttonMap = {}
        
        self.labelMap = {}

        self.x, self.y = -140, 0

        self.i = 0

        self.phase = 'deploy'
        
        self.turns = 0

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
        
        print(territory + ": " + str(self.currentPlayer) + ", " + str(self.currentPlayer.troopsAvailable) + ", " + str(self.map.territories[territory].numberOfTroops))
        availableTerritoriesToAttack = []
        playerOwnedTerritoriesList = []
        
        #player 1
        if self.currentPlayer == self.players[0]:
            if self.phase == 'deploy':
                #cannot change to attack phase until all troops have been deployed
                if self.currentPlayer.troopsAvailable == 0 or self.deployed == True:
                    self.phase = 'attack'
                    self.attacked = False
                    
                    if self.turns > 1:
                        self.buttonMap['phaseButton'].configure(text= 'Attack Phase')
                else:
                    if len(self.map.territories[territory].player) == 0 or self.currentPlayer.label == self.map.territories[territory].player:
                        self.currentPlayer.troopsAvailable -= 1
                        self.map.territories[territory].numberOfTroops += 1
                        self.map.territories[territory].player = self.currentPlayer.label
                        self.buttonMap[territory].configure(text= territory + " " + str(self.map.territories[territory].numberOfTroops)+ '\n' +self.map.territories[territory].player)
            elif self.phase == 'attack': 
                #iterate through territories player owns
                playerOwnedTerritories = ''
                for k, v in self.map.territories.items():
                    if self.map.territories[k].player == self.currentPlayer.label:
                        playerOwnedTerritories += k  + ' -> '
                        playerOwnedTerritoriesList.append(k)
                        for t in self.map.territories[k].adjacentTerritories:
                            if t.player == self.enemy.label:
                                playerOwnedTerritories += t.label + ', '
                                availableTerritoriesToAttack.append(t)
                        playerOwnedTerritories += '\n'

                self.labelMap['territoriesToAttack'].configure(text='territories available to attack from: \n' + playerOwnedTerritories)
                #change from attack to deploy
                if self.attacked or self.turns <= 1:   
                    self.phase = 'deploy'                
                    #after you're done attacking and changed to the next player, give the current player 15 new armies
                    self.currentPlayer = self.players[1] 
                    self.enemy = self.players[0]
                    self.labelMap['playersTurn'].configure(text= self.currentPlayer.label + " turn")
                    if self.turns > 0:
                        self.currentPlayer.troopsAvailable += 15
                    self.turns += 1
                else:
                    #attack one of the available territories
                    #pick a territory to attack from
                    if self.turns > 1:
                        if self.attackingTerritory is not None:                               
                            self.labelMap['attackingTerritoryLabel'].configure(text='attacking territory: ' + str(self.attackingTerritory))                         
                            if self.attackedTerritory is not None:        
                                self.labelMap['attackedTerritoryLabel'].configure(text='territory being attacked: ' + str(self.attackedTerritory))
                                #check if current player has more troops than enemy player, if so, adjust territory accordingly
                                if self.attackingTerritory.numberOfTroops > self.attackedTerritory.numberOfTroops and self.map.territories[territory].player is not self.currentPlayer.label:
                                    self.attackedTerritory.numberOfTroops = 0
                                    self.buttonMap[territory].configure(text= territory + " " + str(1)+ '\n' + self.currentPlayer.label)   
                                    self.attackedTerritory.player = self.currentPlayer                                 
                                    
                                self.buttonMap['phaseButton'].configure(text= 'Deploy Phase')
                            else: 
                                # print('territories avail to attack: ' + str(availableTerritoriesToAttack))
                                if self.map.territories[territory] in availableTerritoriesToAttack:                                    
                                    self.attackedTerritory = self.map.territories[territory]

                        else:
                            #if territory clicked is a territory that the current player owns, then we can attack from it
                            if self.map.territories[territory].label in playerOwnedTerritoriesList:
                                self.attackingTerritory = self.map.territories[territory]

        #player 2
        else:
            if self.phase == 'deploy':
                print('deploy phase')
                #cannot change to attack phase until all troops have been deployed
                if self.currentPlayer.troopsAvailable == 0 or self.deployed == True:
                    self.phase = 'attack'
                    self.attacked = False
                    
                    if self.turns > 1:
                        self.buttonMap['phaseButton'].configure(text= 'Attack Phase')
                else:
                    if len(self.map.territories[territory].player) == 0 or self.currentPlayer.label == self.map.territories[territory].player:
                        self.currentPlayer.troopsAvailable -= 1
                        self.map.territories[territory].numberOfTroops += 1
                        self.map.territories[territory].player = self.currentPlayer.label
                        self.buttonMap[territory].configure(text= territory + " " + str(self.map.territories[territory].numberOfTroops)+ '\n' +self.map.territories[territory].player)
            elif self.phase == 'attack': 
                print('attack phase')                           
                #iterate through territories player owns and append territories that they're able to attack
                playerOwnedTerritories = ''
                #TODO: For some reason North Western Territory isn't showing up as an adjacent territory to Greenland
                for k, v in self.map.territories.items():
                    if self.map.territories[k].player == self.currentPlayer.label:
                        print('player owned territory: ' + str(k), end=', ')
                        playerOwnedTerritories += k  + ' -> '
                        playerOwnedTerritoriesList.append(k)
                        for t in self.map.territories[k].adjacentTerritories:
                            if t.player is not self.currentPlayer.label:                                
                                availableTerritoriesToAttack.append(t.label)
                            else:
                                playerOwnedTerritories += t.label + ', '
                        playerOwnedTerritories += '\n'

                print('adjacent territorites: ' + str(availableTerritoriesToAttack))

                #change label that shows which territories are able to attack
                self.labelMap['territoriesToAttack'].configure(text='territories available to attack from: \n' + playerOwnedTerritories)
                
                #change from attack to deploy if attack phase is done
                if self.attacked or self.turns <= 1:   
                    self.phase = 'deploy'                
                    #after you're done attacking and changed to the next player, give the current player 15 new armies
                    self.currentPlayer = self.players[0] 
                    self.enemy = self.players[1]
                    self.labelMap['playersTurn'].configure(text= self.currentPlayer.label + " turn")
                    if self.turns > 0:
                        self.currentPlayer.troopsAvailable += 15
                    self.turns += 1

                #attack phase is not done
                else:
                    #attack one of the available territories
                    #pick a territory to attack from
                    if self.turns > 1:
                        if self.attackingTerritory is not None:                               
                            self.labelMap['attackingTerritoryLabel'].configure(text='attacking territory: ' + str(self.attackingTerritory))                         
                            if self.attackedTerritory is not None:   
                                self.labelMap['attackedTerritoryLabel'].configure(text='territory being attacked: 2 ' + str(self.attackedTerritory))

                                #check if current player has more troops than enemy player, if so, adjust territory accordingly
                                if self.attackingTerritory.numberOfTroops > self.attackedTerritory.numberOfTroops and self.map.territories[territory].player is not self.currentPlayer.label:
                                    self.attackedTerritory.numberOfTroops = 0
                                    self.buttonMap[territory].configure(text= territory + " " + str(1)+ '\n' + self.currentPlayer.label)   
                                    self.attackedTerritory.player = self.currentPlayer                                 
                                    
                                self.buttonMap['phaseButton'].configure(text= 'Deploy Phase')
                            else: 
                                #if territory clicked is territory that is adjacent to attacking territory then allow it to be the
                                #attacking territory
                                if self.map.territories[territory].label in availableTerritoriesToAttack:        
                                    self.attackedTerritory = self.map.territories[territory]
                        else:
                            #if territory clicked is a territory that the current player owns, then we can attack from it
                            if self.map.territories[territory].label in playerOwnedTerritories:
                                self.attackingTerritory = self.map.territories[territory]


    def isDoneAttacking(self):

        self.phase = 'deploy'                
        #after you're done attacking and changed to the next player, give the current player 15 new armies
        self.labelMap['playersTurn'].configure(text= self.currentPlayer.label + " turn")

        self.attacked = True
        self.isDoneAttackingPressed = False
        
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
            self.enemy = self.player1
        else:
            self.currentPlayer = self.player1
            self.enemy = self.player2
        # self.map.territories[territory].player = self.currentPlayer.label
        self.deployed = False
        self.attackedTerritory = None
        self.attackingTerritory = None
        self.isDoneAttackingPressed = True        

        if self.turns > 0:
            self.currentPlayer.troopsAvailable += 15
        self.turns += 1
    
    def startGame(self):          
        for k, v in self.map.territories.items():
        # for k in range(5):
            if (self.i % 10) == 0:
                self.x += 200
                self.y = 0
            else:
                self.y += 35

            self.i += 1
            t = Button(self.root, text = str(k) + " " + str(self.map.territories[k].numberOfTroops) + '\n' +self.map.territories[k].player, height=2, width=18, bd = '2', command = partial(self.selectTerritory, k))
            t.place(x=self.x, y=self.y)
            t['font'] = self.myFont
            self.buttonMap[k] = t


        phase = Button(self.root, text = 'Deploy Phase', height= 2, width= 18, bd= '2', command=(self.nextPhase))
        phase.place(x=100, y=400)
        self.buttonMap['phaseButton'] = phase

        isDoneAttacking = Button(self.root, text='press if done attacking', height=2, width= 18, command=(self.isDoneAttacking))
        isDoneAttacking.place(x=100, y=500)
        self.buttonMap['isDoneAttacking'] = isDoneAttacking

        territoriesToAttack = Label(self.root, text= '')
        territoriesToAttack.place(x=1080/2, y=400)
        self.labelMap['territoriesToAttack'] = territoriesToAttack        

        playersTurn = Label(self.root, text= self.currentPlayer.label + ' turn')
        playersTurn.place(x=1080/2, y=350)
        self.labelMap['playersTurn'] = playersTurn

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


newGame = Game()
newGame.startGame()