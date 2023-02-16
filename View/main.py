from tkinter import *
import tkinter.font as font
import sys
sys.path.insert(0,"..")
from Models.Map import map

root = Tk()

root.geometry('1080x1080')

myFont = font.Font(size=8)

map = map('bob')
x, y = -140, 0
i = 0
for k, v in map.territories.items():
# for k in range(5):
    if (i % 10) == 0:
        x += 200
        y = 0
    else:
        y += 35

    i += 1
    t = Button(root, text = str(k), height=1, width=15, bd = '2', command = None)
    t.place(x=x, y=y)
    t['font'] = myFont
                        
root.mainloop()