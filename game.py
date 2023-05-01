import time
import pygame
from pygame.locals import *
import board

pygame.init()

# size = width, height = 320, 240
size = width, height = 500, 300
white = (255, 255, 255)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


board_size = 4
game_board = board.Board()
game_board.add_tile()
text_font = game_board.get_font(height, 3)

tile_height = height // (game_board.side + 1)
tile_width = width // (game_board.side + 1)
to_shift = tile_width // 2

# text buttons
text_buttons = ["Score", "New Game", "Quit"]
text_buttons_dict = []
for i in range(len(text_buttons)):
    text = text_font.render(text_buttons[i], True, white)
    rect = text.get_rect(centerx=width - tile_width +
                         to_shift, y=i * tile_height + to_shift // 2)
    text_buttons_dict.append((text_buttons[i], (text, rect)))
text_buttons_dict = dict(text_buttons_dict)
# {"Quit" : (quit_text, quit_rect)}


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


quit_clicked = False
running = True
try:
    game_status = (False, "")
    while running and not quit_clicked:
        screen.blit(text_buttons_dict["Quit"][0], text_buttons_dict["Quit"][1])
        screen.blit(text_buttons_dict["Score"][0],
                    text_buttons_dict["Score"][1])
        screen.blit(text_buttons_dict["New Game"]
                    [0], text_buttons_dict["New Game"][1])
        game_board.draw(screen, width, height, clock)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                dir = key_to_dir(event.unicode)
                if dir is not None:
                    if game_board.shift(dir):
                        game_board.add_tile()
                        game_status = game_board.end()
                    running = not game_status[0]
            if event.type == MOUSEBUTTONDOWN:
                quit_clicked = text_buttons_dict["Quit"][1].collidepoint(
                    event.pos)
                new_game_clicked = text_buttons_dict["New Game"][1].collidepoint(
                    event.pos)
                if new_game_clicked:
                    game_board = board.Board()
                    game_board.add_tile()

    print(game_status[1])
finally:
    pygame.quit()
