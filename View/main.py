from tkinter import *
import sys
sys.path.insert(0,"..")
# from Models.button import Button
from Models.Map import map

root = Tk()

root.geometry('1080x1080')

map = map('bob')
x, y = 0, 0
i = 0
for k, v in map.territories.items():
# for k in range(5):
    if (i % 20) == 0:
        x += 250
        y = 0
    else:
        y += 35

    i += 1
    print(k)
    Button(root, text = str(k), bd = '5',
						command = root.destroy).place(x=x, y=y)
root.mainloop()