import time
import pygame
from pygame.locals import *
import board
import api

pygame.init()


class Leaderboard:
    def __init__(self, width, height, font, font_color):
        self.back_clicked = False
        self.back_text = font.render("Back", True, font_color)
        self.back_rect = self.back_text.get_rect(centerx=width // 2, y=height)

    def handle_events(self):
        for event in pygame.event.get():
            self.back_clicked = self.back_rect.collidepoint(event.pos)
        # return self.back_clicked
        return False

    def draw(self, screen, clock, width, height, font, font_color):
        limit = 10
        all_scores = api.all_high_scores(limit=limit)
        i = 0
        for place in all_scores:
            print(place["score"])
            username_text = font.render(
                place["username"], True, font_color)
            username_rect = username_text.get_rect(
                centerx=width // 4, y=(height * i // limit + limit))
            score_text = font.render(str(place["score"]), True, font_color)
            score_rect = score_text.get_rect(
                centerx=width * 3 // 4, y=height * i // limit + limit)
            screen.blit(username_text, username_rect)
            screen.blit(score_text, score_rect)

        screen.blit(self.back_text, self.back_rect)
