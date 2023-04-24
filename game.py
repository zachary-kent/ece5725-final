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

def key_to_dir(key):
    if key == 'w':
        return board.Dir.UP
    if key == 's':
        return board.Dir.DOWN
    if key == 'a':
        return board.Dir.LEFT
    if key == 'd':
      return board.Dir.RIGHT
    return None

running = True
try:
    while running:
        game_board.draw(screen, width, height, clock)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                board.shift(key_to_dir(event.unicode))
                
                
finally:
    pygame.quit()
