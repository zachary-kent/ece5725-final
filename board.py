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
black = (0, 0, 0)
gray = (169, 169, 169)
tile_empty = (204, 192, 179)
tile_2 = (238, 228, 218)
tile_4 = (237, 224, 200)
tile_8 = (242, 177, 121)
tile_16 = (245, 149, 99)
tile_32 = (246, 124, 95)
tile_64 = (246, 94, 59)
tile_128 = (237, 207, 114)
tile_256 = (237, 204, 97)
tile_512 = (237, 200, 80)
tile_1024 = (237, 197, 63)
tile_2048 = (237, 194, 46)

tile_colors = [tile_empty, tile_2, tile_4, tile_8, tile_16, tile_32,
               tile_64, tile_128, tile_256, tile_512, tile_1024, tile_2048]


class Board:
    def __init__(self, side):
        self.side = side
        self.board = create_board(side)
        self.score = 0

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

    def draw(self, screen, width, height, clock):
        count = 0
        font_size = height // self.side // 2
        font = pygame.font.Font(None, font_size)
        tile_height = height // self.side
        tile_width = width // self.side
        for i in range(self.side):
            for j in range(self.side):
                tile_exponent = self.at(i, j)
                to_shift = tile_width / 2
                tileX = i * tile_width + to_shift
                tileY = j * tile_height + to_shift / 2

                tile_color = tile_colors[tile_exponent + count]
                if count < len(tile_colors) - 2:
                    count = count + 0
                else:
                    count = 0

                text_color = white
                if tile_color == tile_2 or tile_color == tile_4:
                    text_color = gray

                tile = pygame.draw.rect(screen, tile_color, (tileX - to_shift,
                                                             tileY - to_shift / 2, tile_width, tile_height))

                tile_number = 2 ** tile_exponent
                # if no number, then text is ""]
                tile_text = font.render(str(tile_number), True,
                                        text_color) if tile_number != 1 else font.render("", True,
                                                                                         text_color)
                tile_rect = tile_text.get_rect(centerx=tileX, y=tileY)
                screen.blit(tile_text, tile_rect)

        # draw vertical and horizontal separating lines
        for i in range(2):
            for j in range(self.side + 3):
                if i == 0:  # horizontal
                    pygame.draw.line(
                        screen, white, (0, j * tile_height), (width, j * tile_height))
                else:  # vertical
                    pygame.draw.line(
                        screen, white, (j * tile_width, 0), (j * tile_width, height))

        pygame.display.flip()
        clock.tick(60)

    def test_gui(self):
        for i in range(self.side):
            for j in range(self.side):
                self.board[i][j] = 0
