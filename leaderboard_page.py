import time
import pygame
from pygame.locals import *
import board
import api

pygame.init()


class Leaderboard:
    def __init__(self, width, height, font, font_color, limit):
        self.back_text = font.render("Back", True, font_color)
        self.back_rect = self.back_text.get_rect(
            centerx=width // 2, y=height - (height // limit))
        self.limit = limit

    def handle_events(self):
        back_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                back_clicked = self.back_rect.collidepoint(event.pos)
        return back_clicked

    def draw(self, screen, clock, width, height, font, font_color):
        all_scores = api.all_high_scores(limit=self.limit)
        i = 0
        for place in all_scores:
            place_text = font.render(str(i + 1), True, font_color)
            place_rect = place_text.get_rect(
                centerx=width//8, y=(height * i // self.limit + self.limit))
            screen.blit(place_text, place_rect)
            username_text = font.render(
                place["username"], True, font_color)
            username_rect = username_text.get_rect(
                centerx=width // 4, y=(height * i // self.limit + self.limit))
            score_text = font.render(str(place["score"]), True, font_color)
            score_rect = score_text.get_rect(
                centerx=width * 3 // 4, y=height * i // self.limit + self.limit)
            screen.blit(username_text, username_rect)
            screen.blit(score_text, score_rect)
            i = i + 1

        screen.blit(self.back_text, self.back_rect)
