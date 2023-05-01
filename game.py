import time
import pygame
from pygame.locals import *
import board

pygame.init()

size = width, height = 320, 240
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


board_size = 4
game_board = board.Board()
game_board.add_tile()


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
    game_status = (False, "")
    while running:
        game_board.draw(screen, width, height, clock)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                dir = key_to_dir(event.unicode)
                if dir is not None:
                    if game_board.shift(dir):
                        game_board.add_tile()
                        game_status = game_board.end()
                    running = not game_status[0]
    print(game_status[1])
finally:
    pygame.quit()
