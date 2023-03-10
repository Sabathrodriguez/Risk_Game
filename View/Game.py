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
        
        #player 1
        if self.currentPlayer == self.players[0]:
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
                #iterate through territories player owns
                playerOwnedTerritories = ''
                for k, v in self.map.territories.items():
                    if self.map.territories[k].player == self.currentPlayer.label:
                        playerOwnedTerritories += k  + ' -> '
                        for t in self.map.territories[k].adjacentTerritories:
                            if t.player == self.enemy.label:
                            # print('t: ' + t.label + 't.player: ' + t.player + ", " + self.enemy.label)                            
                                playerOwnedTerritories += t.label + ', '
                                availableTerritoriesToAttack.append(t)
                        playerOwnedTerritories += '\n'

                self.labelMap['territoriesToAttack'].configure(text='territories available to attack from: \n' + playerOwnedTerritories)
                #change from attack to deploy
                if self.attacked or self.turns == 0:   
                    print('1-1')             
                    self.phase = 'deploy'                
                    #after you're done attacking and changed to the next player, give the current player 15 new armies
                    self.currentPlayer = self.players[1] 
                    self.enemy = self.players[0]
                    self.labelMap['playersTurn'].configure(text= self.currentPlayer.label + " turn")
                    if self.turns > 0:
                        self.currentPlayer.troopsAvailable += 15
                    self.turns += 1
                else:
                    print('1-2')
                    #attack one of the available territories
                    #pick a territory to attack from
                    if self.turns > 0:
                        print('1-3')
                        if self.attackingTerritory is not None:                               
                            self.labelMap['attackingTerritoryLabel'].configure(text='attacking territory: ' + str(self.attackingTerritory))                         
                            if self.attackedTerritory is not None:        
                                self.labelMap['attackedTerritoryLabel'].configure(text='territory being attacked: ' + str(self.attackedTerritory))
                                print('1-6')                        
                                if self.attackingTerritory.numberOfTroops > self.attackedTerritory.numberOfTroops:
                                    print('1-7')
                                    self.attackedTerritory.numberOfTroops = 0
                                    self.buttonMap[territory].configure(text= territory + " " + str(1)+ '\n' + self.currentPlayer.label)   
                                    self.attackedTerritory.player = self.currentPlayer                                 
                                    
                                self.buttonMap['phaseButton'].configure(text= 'Deploy Phase')
                            else: 
                                print('1-5')
                                print('territories avail to attack: ' + str(availableTerritoriesToAttack))
                                if self.map.territories[territory] in availableTerritoriesToAttack:                                    
                                    self.attackedTerritory = self.map.territories[territory]
                                    print('attacked terr: ' + self.attackedTerritory.label)
                        else:
                            print('1-4')
                            self.attackingTerritory = self.map.territories[territory]
                            print('terr: ' + territory)
                            print('attacking terr: ' + self.attackingTerritory.label)
                        print('attack')

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
                        print('no player: ' + str(len(self.map.territories[territory].player) == 0))
                        print('is same player: ' + str(self.currentPlayer.label == self.map.territories[territory].player))
                        self.currentPlayer.troopsAvailable -= 1
                        self.map.territories[territory].numberOfTroops += 1
                        self.map.territories[territory].player = self.currentPlayer.label
                        self.buttonMap[territory].configure(text= territory + " " + str(self.map.territories[territory].numberOfTroops)+ '\n' +self.map.territories[territory].player)
            elif self.phase == 'attack': 
                print('attack phase')                           
                #iterate through territories player owns
                playerOwnedTerritories = ''
                for k, v in self.map.territories.items():
                    if self.map.territories[k].player == self.currentPlayer.label:
                        playerOwnedTerritories += k  + ' -> '
                        for t in self.map.territories[k].adjacentTerritories:
                            if t.player == self.enemy.label:
                                playerOwnedTerritories += t.label + ', '
                                availableTerritoriesToAttack.append(t)
                        playerOwnedTerritories += '\n'

                self.labelMap['territoriesToAttack'].configure(text='territories available to attack from: \n' + playerOwnedTerritories)
                #change from attack to deploy
                if self.attacked or self.turns == 0:   
                    print('1')             
                    self.phase = 'deploy'                
                    #after you're done attacking and changed to the next player, give the current player 15 new armies
                    self.currentPlayer = self.players[0] 
                    self.enemy = self.players[1]
                    self.labelMap['playersTurn'].configure(text= self.currentPlayer.label + " turn")
                    if self.turns > 0:
                        self.currentPlayer.troopsAvailable += 15
                    self.turns += 1
                else:
                    print('2')
                    #attack one of the available territories
                    #pick a territory to attack from
                    if self.turns > 0:
                        print('3')
                        if self.attackingTerritory is not None:                            
                            if self.attackedTerritory is not None:                                
                                if self.attackingTerritory.numberOfTroops > self.attackedTerritory.numberOfTroops:
                                    self.attackedTerritory.numberOfTroops = 0
                                    self.buttonMap[territory].configure(text= territory + " " + str(1)+ '\n' + self.currentPlayer.label)
                                    
                                self.attacked = True
                                self.deployed = False
                                self.attackedTerritory = None
                                self.attackingTerritory = None
                                self.buttonMap['phaseButton'].configure(text= 'Deploy Phase')
                            else:
                                if self.map.territories[territory] in availableTerritoriesToAttack:                                    
                                    self.attackedTerritory = self.map.territories[territory]
                                    print('attacked terr: ' + self.attackedTerritory.label)
                        else:
                            print('4')
                            self.attackingTerritory = self.map.territories[territory]
                            print('terr: ' + territory)
                            print('attacking terr: ' + self.attackingTerritory.label)
                        print('attack')

    def isDoneAttacking(self):
        print('1-8')                       
        self.attacked = True
        self.isDoneAttackingPressed = False
        
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1
        # self.map.territories[territory].player = self.currentPlayer.label
        self.deployed = False
        self.attackedTerritory = None
        self.attackingTerritory = None
        self.isDoneAttackingPressed = True        
    
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