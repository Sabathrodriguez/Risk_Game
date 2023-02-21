from tkinter import *
import tkinter.font as font
import sys
sys.path.insert(0,"..")
from Models.Map import map
from Models.Player import Player
from functools import partial

class Game:
    
    def __init__(self):
        self.player1 = Player('Player 1', 10)
        self.player2 = Player('Player 2', 10)

        self.players = [self.player1, self.player2]

        self.currentPlayer = self.players[0]

        self.root = Tk()

        self.root.geometry('1080x1080')

        self.myFont = font.Font(size=8)

        self.map = map(self.players)

        self.x, self.y = -140, 0

        self.i = 0

        self.phase = 'deploy'

    def open_popup(self, text):
        top= Toplevel(self.root)
        top.geometry("250x750")
        top.title("phase")
        Label(top, text= text, font=('Mistral 18 bold')).place(x=150,y=80)

    def selectTerritory(self, territory):    
        
        print(territory + ": " + str(self.currentPlayer))
        
        if self.currentPlayer == self.players[0]:
            if self.phase == 'deploy':
                self.phase = 'attack'
            elif self.phase == 'attack':
                self.phase = 'deploy'
                self.currentPlayer = self.players[1]
        else:
            if self.phase == 'deploy':
                self.phase = 'attack'
            elif self.phase == 'attack':
                self.phase = 'deploy'
                self.currentPlayer = self.players[0]  
    
    def startGame(self):          
        for k, v in self.map.territories.items():
        # for k in range(5):
            if (self.i % 10) == 0:
                self.x += 200
                self.y = 0
            else:
                self.y += 35

            self.i += 1
            t = Button(self.root, text = str(k), height=1, width=15, bd = '2', command = partial(self.selectTerritory, k))
            t.place(x=self.x, y=self.y)
            t['font'] = self.myFont

        self.root.mainloop()

newGame = Game()
newGame.startGame()