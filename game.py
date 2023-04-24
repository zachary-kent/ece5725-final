import time
import pygame
from pygame.locals import *
import board

pygame.init()

size = width, height = 320, 240
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


board_size = 4
game_board = board.Board([
    [1, 1, 0, 1],
    [2, 1, 0, 0],
    [2, 1, 0, 0],
    [2, 1, 0, 0],
])

running = True
try:
    while running:
        game_board.draw(screen, width, height, clock)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                print(event.key)
                
                
finally:
    pygame.quit()
