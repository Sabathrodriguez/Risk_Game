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

        self.x, self.y = -140, 0

        self.i = 0

        self.phase = 'deploy'
        
        self.turns = 0

    def open_popup(self, text):
        top= Toplevel(self.root)
        top.geometry("250x750")
        top.title("phase")
        Label(top, text= text, font=('Mistral 18 bold')).place(x=150,y=80)

    def selectTerritory(self, territory):    
        
        print(territory + ": " + str(self.currentPlayer) + ", " + str(self.currentPlayer.troopsAvailable) + ", " + str(self.map.territories[territory].numberOfTroops))
        
        if self.currentPlayer == self.players[0]:
            if self.phase == 'deploy':
                #cannot change to attack phase until all troops have been deployed
                if self.currentPlayer.troopsAvailable == 0:
                    self.phase = 'attack'
                else:
                    if len(self.map.territories[territory].player) == 0 or self.currentPlayer.label == self.map.territories[territory].player:
                        self.currentPlayer.troopsAvailable -= 1
                        self.map.territories[territory].numberOfTroops += 1
                        self.map.territories[territory].player = self.currentPlayer.label
                        self.buttonMap[territory].configure(text= territory + " " + str(self.map.territories[territory].numberOfTroops)+ '\n' +self.map.territories[territory].player)
            elif self.phase == 'attack':
                self.phase = 'deploy'                
                #after you're done attacking and changed to the next player, give the current player 15 new armies
                self.currentPlayer = self.players[1] 
                if self.turns > 0:
                    self.currentPlayer.troopsAvailable += 15
                self.turns += 1
        else:
            if self.phase == 'deploy':
                #cannot change to attack phase until all troops have been deployed
                if self.currentPlayer.troopsAvailable == 0:
                    self.phase = 'attack'
                else:
                    if len(self.map.territories[territory].player) == 0 or self.currentPlayer.label == self.map.territories[territory].player:
                        self.currentPlayer.troopsAvailable -= 1
                        self.map.territories[territory].numberOfTroops += 1
                        self.map.territories[territory].player = self.currentPlayer.label
                        self.buttonMap[territory].configure(text= territory + " " + str(self.map.territories[territory].numberOfTroops)+ '\n' +self.map.territories[territory].player)
            elif self.phase == 'attack':
                self.phase = 'deploy'                
                #after you're done attacking and changed to the next player, give the current player 15 new armies
                self.currentPlayer = self.players[0] 
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

        self.root.mainloop()

newGame = Game()
newGame.startGame()