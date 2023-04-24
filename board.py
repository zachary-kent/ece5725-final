import pygame
import numpy as np
from enum import Enum
import enum


class Dir(Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    # def angle(self):
    #     match self:
    #         case self.UP:
    #             return 1
    #         case self.DOWN:
    #             return -1
    #         case self.LEFT:
    #             return 2
    #         case self.RIGHT:
    #             return 0


def create_board(side):
    return np.zeros((side, side), int)


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



class Board:
    def __init__(self, side):
        self.side = side
        self.board = create_board(side)

    def in_bounds(self, i, j):
        return 0 <= i < self.side and 0 <= j < self.side

    def erase(self, i, j):
        self.board[i][j] = 0

    def is_empty(self, i, j):
        return self.at(i, j) == 0

    def shift_tile(self, i, j):
        tiles_moved = 0
        # Value of tile we are shifting across board
        tile_value = self.at(i, j)
        # Erase current tile
        self.erase(i, j)
        # Move tile while in bounds and next position is unoccupied
        while self.in_bounds(i + 1, j) and self.is_empty(i + 1, j):
            tiles_moved += 1
            i += 1
        # Set value at tile with position moved to
        self.board[i][j] = tile_value
        # Combine with tile to right if exists and has same value
        if self.in_bounds(i + 1, j) and self.at(i, j) == self.at(i + 1, j):
            self.erase(i, j)
            self.board[i + 1][j] += 1
            tiles_moved += 1
        return tiles_moved

    def shift_right(self):
        for i in range(self.side):
            for j in range(self.side):
                tiles_moved = self.shift_tile(i, j)
                pass

    def shift(self, dir: Dir):
        angle = dir.angle()

    def at(self, i, j):
        return self.board[i][j]

    def draw(self, screen, width, height):
        font_size = height // self.side // 5
        font = pygame.font.Font(None, font_size)
        tile_size = height // self.side
        for i in range(self.side):
            for j in range(self.side):
                tile_exponent = self.at(i, j)
                tileX = i / self.side * width
                tileY = j / self.side * height
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
        

    def test_gui(self):
        for i in range(self.side):
            for j in range(self.side):
                self.board[i][j] = 1
