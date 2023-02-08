import pygame
import sys
sys.path.insert(0,"..")
from Models.button import Button

#initialize pygame import for use
pygame.init()

#screen setup for game
width, height = 1080, 1080
screen = pygame.display.set_mode((width, height))
fps = 60
fpsClock = pygame.time.Clock()

#font for game
font = pygame.font.SysFont('Arial', 40)

#territories list
territories = []

#action for when button/territory is pressed
def myFunction():
    print('Button Pressed')

alaska = Button(30, 30, 400, 100, 'Alaska', myFunction, False, font)
NWTerritory = Button(30, 250, 400, 100, 'North Western Territory', myFunction, False, font)

territories.append(alaska)
territories.append(NWTerritory)

#keep game open and iterate through territories to process changes
while True:
    screen.fill((20, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for object in territories:
        object.process(screen)
    pygame.display.flip()
    fpsClock.tick(fps)