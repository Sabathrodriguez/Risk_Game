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

        self.root.geometry('1080x1080')

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


    #TODO: fix bug the allows attacking player to continue taking over territories after winning a battle
    def selectTerritory(self, territory):    
        
        print(territory + ": " + str(self.currentPlayer) + ", " + str(self.currentPlayer.troopsAvailable) + ", " + str(self.map.territories[territory].numberOfTroops))
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
                print('deploy phase')
                #cannot change to attack phase until all troops have been deployed
                self.deployPhase(territory)
            elif self.phase == 'attack': 
                print('attack phase')                           
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
        # self.map.territories[territory].player = self.currentPlayer.label
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


        #initialize territories
        for k, v in self.map.territories.items():
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

    def attackPhase(self, player, playerOwnedTerritoriesList, availableTerritoriesToAttack, territory):
        playerOwnedTerritories = ''
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

        
        if self.attackingTerritory is not None:                               
            self.labelMap['attackingTerritoryLabel'].configure(text='attacking territory: ' + str(self.attackingTerritory))                         
            if self.attackedTerritory is not None:        
                self.labelMap['attackedTerritoryLabel'].configure(text='territory being attacked: ' + str(self.attackedTerritory))
                #check if current player has more troops than enemy player, if so, adjust territory accordingly
                if self.attackingTerritory.numberOfTroops > self.attackedTerritory.numberOfTroops and self.map.territories[territory].player is not self.currentPlayer.label:
                    self.attackedTerritory.numberOfTroops = 0
                    self.buttonMap[territory].configure(text= territory + " " + str(1)+ '\n' + self.currentPlayer.label)   
                    self.attackedTerritory.player = self.currentPlayer                                 
                    
            else: 
                # print('territories avail to attack: ' + str(availableTerritoriesToAttack))
                if self.map.territories[territory].label in availableTerritoriesToAttack:                                    
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
            if len(self.map.territories[territory].player) == 0 or self.currentPlayer.label == self.map.territories[territory].player:
                print('DEPLOY PHASE')
                self.currentPlayer.troopsAvailable -= 1
                self.map.territories[territory].numberOfTroops += 1
                self.map.territories[territory].player = self.currentPlayer.label
                self.buttonMap[territory].configure(text= territory + " " + str(self.map.territories[territory].numberOfTroops)+ '\n' +self.map.territories[territory].player)

newGame = Game()
newGame.startGame()