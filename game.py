import time
import pygame
import board

pygame.init()

size = width, height = 320, 240
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


board_size = 4
game_board = board.Board(board_size)


# draw board
game_board.test_gui()
running = True
try:
  while running:
    game_board.draw(screen, width, height)
finally:

  pygame.quit()
