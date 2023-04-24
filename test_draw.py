import pygame
import numpy as np

pygame.init()

white = (255, 255, 255)
gray = (169, 169, 169)
light_gray = (211, 211, 211)
beige = (207, 185, 151)
light_orange = (255, 213, 128)
orange = (255, 165, 0)
light_red = (255, 204, 203)
red = (255, 0, 0)
light_yellow = (255, 255, 191)
# 2, 4, 8, 16, 32, 64, 128
tile_colors = [gray, light_gray, beige, light_orange,
               orange, light_red, red, light_yellow]

size = width, height = 320, 240
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

side = 4

board = np.zeros((side, side), int)

# populate board
for i in range(side):
    for j in range(side):
        board[i][j] = 1


def draw():
    font_size = height // side // 5
    font = pygame.font.Font(None, font_size)
    tile_size = height // side
    for i in range(side):
        for j in range(side):
            tile_exponent = board[i][j]
            tileX = i / side * width
            tileY = j / side * height
            tile_color = tile_colors[tile_exponent]
            tile = pygame.draw.rect(screen, tile_color, (tileX - tile_size / 2,
                                                         tileX + tile_size / 2, tileY - tile_size / 2, tileY + tile_size / 2))

            tile_number = 2 ** tile_exponent
            # if no number, then text is ""
            tile_text = font.render(str(tile_number), True,
                                    white) if tile_number != 1 else ""
            tile_rect = tile_text.get_rect(centerx=tileX, y=tileY)
            screen.blit(tile_text, tile_rect)
    pygame.display.flip()


running = True
try:
    while running:
        draw()
finally:

    pygame.quit()
