import time
import pygame
from pygame.locals import *
import board
import api

pygame.init()


class Login:
    def __init__(self, width, height, font, colors):
        self.login_clicked = False
        self.create_clicked = False
        self.username_clicked = False
        self.password_clicked = False
        self.create_success = False
        self.login_failed = False

        # login / create account screen
        self.width = width
        self.height = height
        self.colors = colors
        self.font = font

        # username / password text boxes
        self.username_text = ''
        self.username_rect = pygame.Rect(
            width // 4, height // 6, width // 2, 32)
        self.password_text = ''
        self.password_rect = pygame.Rect(
            width // 4, height * 2 // 6, width // 2, 32)

        # login button
        self.login_text = font.render("Login", True, colors["white"])
        self.login_rect = self.login_text.get_rect(
            centerx=width // 2, y=height * 3 // 6)

        # create account button
        self.create_text = font.render("Create Account", True, colors["white"])
        self.create_rect = self.create_text.get_rect(
            centerx=width // 2, y=height * 4 // 6)

        # success text for creating account
        self.success_text = font.render("Success!", True, colors["white"])
        self.success_rect = self.success_text.get_rect(
            centerx=width // 2, y=(height * 5 // 6))

        # failed login
        self.login_failed_text = font.render(
            "Incorrect username or password", True, colors["white"])
        self.login_failed_rect = self.login_failed_text.get_rect(
            centerx=width // 2, y=(height * 5 // 6))

    def draw(self, screen, clock):
        # username text box
        username_box_color = self.colors["gray"] if not self.username_clicked else self.colors["white"]
        pygame.draw.rect(screen, username_box_color, self.username_rect)
        username_surface = self.font.render(
            self.username_text, True, self.colors["black"])
        screen.blit(username_surface,
                    (self.username_rect.x+5, self.username_rect.y+5))
        self.username_rect.w = max(
            self.width // 2, username_surface.get_width()+10)

        # password text box
        password_box_color = self.colors["gray"] if not self.password_clicked else self.colors["white"]
        pygame.draw.rect(screen, password_box_color, self.password_rect)
        password_surface = self.font.render(
            self.password_text, True, self.colors["black"])
        screen.blit(password_surface,
                    (self.password_rect.x+5, self.password_rect.y+5))
        self.password_rect.w = max(
            self.width // 2, password_surface.get_width()+10)

        # login button
        screen.blit(self.login_text, self.login_rect)
        # create account button
        screen.blit(self.create_text, self.create_rect)
        # if success at creating account, display 'success' message
        if self.create_success:
            screen.blit(self.success_text, self.success_rect)
        elif self.login_failed:
            screen.blit(self.login_failed_text,
                        self.login_failed_rect)

        pygame.display.flip()
        clock.tick(60)

    def handle_events(self, screen, clock):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.username_clicked = self.username_rect.collidepoint(
                    event.pos)
                self.password_clicked = self.password_rect.collidepoint(
                    event.pos)
                self.login_clicked = self.login_rect.collidepoint(event.pos)
                if self.login_clicked:
                    try:
                        user = api.User(self.username_text, self.password_text)
                        self.login_success = True
                        return False
                    except api.InvalidCredentialsError:
                        self.login_clicked = False
                        self.login_failed = True
                        return True
                self.create_clicked = self.create_rect.collidepoint(event.pos)
                if self.create_clicked:
                    self.create_success = api.create_account(
                        self.username_text, self.password_text)

            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    if self.username_clicked:
                        self.username_text = self.username_text[:-1]
                    elif self.password_clicked:
                        self.password_text = self.password_text[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    if self.username_clicked:
                        self.username_text += event.unicode
                    elif self.password_clicked:
                        self.password_text += event.unicode

        return True

    def login(self):
        self.create_success = False
        return True

    def createAccount(self):
        return True
