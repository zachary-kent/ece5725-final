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


def createAccount():
    return [True, "Success"]


# login / create account screen
login_text = text_font.render("Login", True, white)
login_rect = login_text.get_rect(centerx=width // 2, y=height // 4)
create_text = text_font.render("Create Account", True, white)
create_rect = create_text.get_rect(centerx=width // 2, y=height // 2)
success_text = text_font.render(createAccount()[1], True, white)
success_rect = success_text.get_rect(centerx=width // 2, y=(height * (3 // 4)))

login_clicked = False
create_clicked = createAccount()[0]

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
        if not create_clicked:
            screen.blit(login_text, login_rect)
            screen.blit(create_text, create_rect)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    create_clicked = create_rect.collidepoint(event.pos)
            if create_clicked:
                screen.blit(success_text, success_rect)
            pygame.display.flip()
            clock.tick(60)
        elif not login_clicked:
            screen.blit(login_text, login_rect)
            screen.blit(create_text, create_rect)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    login_clicked = login_rect.collidepoint(event.pos)
            pygame.display.flip()
            clock.tick(60)
        else:
            screen.blit(text_buttons_dict["Quit"]
                        [0], text_buttons_dict["Quit"][1])
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
