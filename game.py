import time
import pygame
from pygame.locals import *
import board
import login_page
import leaderboard_page
import sys
import os

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

pygame.init()

size = width, height = 320, 240
#size = width, height = 500, 300
white = (255, 255, 255)
black = (0, 0, 0)
gray = (169, 169, 169)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

BUTTONS = [22, 27, 17, 23]


TFT = False

if TFT:
    GPIO.setmode(GPIO.BCM)   # Set for GPIO (bcm) numbering not pin numbers...
    for button in BUTTONS:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Display on piTFT
    # os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
    # os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# pygame.mouse.set_visible(not TFT)


def button_to_dir(button):
    if button == 17:
        return board.Dir.UP
    if button == 22:
        return board.Dir.DOWN
    if button == 23:
        return board.Dir.LEFT
    if button == 27:
        return board.Dir.RIGHT
    return None


board_size = 4
game_board = board.Board()
game_board.add_tile()
login_text_font = game_board.get_font(height, 2)
playing_text_font = game_board.get_font(height, 4)

tile_height = height // (game_board.side + 1)
tile_width = width // (game_board.side + 1)
to_shift = tile_width // 2

login = login_page.Login(width, height, login_text_font, {
                         "white": white, "black": black, "gray": gray})

leaderboard = leaderboard_page.Leaderboard(
    width, height, login_text_font, white, 7)

# text buttons
text_buttons = ["Score: 0", "New Game", "Quit", "Scores", "Logout"]
text_buttons_dict = []
for i in range(len(text_buttons)):
    text = playing_text_font.render(text_buttons[i], True, white)
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
login_screen = True
user = None
topscores_clicked = False
logout_clicked = False
try:
    game_status = (False, "")
    while running and not quit_clicked:
        screen.fill(black)
        if login_screen:
            login.draw(screen)
            user = login.handle_events()
            login_screen = user is None
        elif logout_clicked:
            logout_clicked = False
            login_screen = True
            user.set_high_score(int(game_board.score))
            user = None
            game_board = board.Board()
            game_board.add_tile()
        elif topscores_clicked:
            leaderboard.draw(screen, clock, width, height,
                             playing_text_font, white)
            topscores_clicked = not leaderboard.handle_events()
        else:
            dir = None
            if TFT:
                for button in BUTTONS:
                    if not GPIO.input(button):
                        dir = button_to_dir(button)
            for text, rect in text_buttons_dict.values():
                screen.blit(text, rect)
            game_board.draw(screen, width, height)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    dir = key_to_dir(event.unicode)

                if event.type == MOUSEBUTTONDOWN:
                    quit_clicked = text_buttons_dict["Quit"][1].collidepoint(
                        event.pos)
                    new_game_clicked = text_buttons_dict["New Game"][1].collidepoint(
                        event.pos)
                    topscores_clicked = text_buttons_dict["Scores"][1].collidepoint(
                        event.pos)
                    logout_clicked = text_buttons_dict["Logout"][1].collidepoint(
                        event.pos)
                    if new_game_clicked:
                        score_text = playing_text_font.render(
                            "Score: 0", True, white)
                        score_rect = score_text.get_rect(centerx=width - tile_width +
                                                         to_shift, y=to_shift // 2)
                        text_buttons_dict["Score"] = (
                            score_text, score_rect)
                        game_board = board.Board()
                        game_board.add_tile()
            if dir is not None:
                if game_board.shift(dir):
                    game_board.add_tile()
                    score_text = playing_text_font.render(
                        "Score: " + str(game_board.score), True, white)
                    score_rect = score_text.get_rect(centerx=width - tile_width +
                                                     to_shift, y=to_shift // 2)
                    text_buttons_dict["Score: 0"] = (
                        score_text, score_rect)
        pygame.display.flip()
        clock.tick(60)
    if user is not None:
        user.set_high_score(int(game_board.score))
finally:
    pygame.quit()
    GPIO.cleanup()
