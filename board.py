#
# zak33, nnb28, 5/17/23: board.py
# 
# Represents an abstract board in 2048; comprises the majority of the
# game logic
#

import pygame
import numpy as np
from enum import Enum
import enum
import random

# Represents a cardinal direction
class Dir(Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    # Calculates the angle to 180 degrees, in units of 90 degrees
    def angle_to_left(self):
        if self == Dir.UP:
            return 1
        if self == Dir.DOWN:
            return -1
        if self == Dir.LEFT:
            return 0
        if self == Dir.RIGHT:
            return 2


def create_board(side):
    return np.zeros((side, side), int)

# Filter out the zero elements of a given array, leaving only the nonzero elements


def filter_nonzeros(arr):
    nonzeros = []
    for i in arr:
        if i != 0:
            nonzeros.append(i)
    return nonzeros


# Shifts a row left according to 2048 semantics and returns the resulting row
# Empty tiles are represented with zeros
def shift_row(row):
    nonzeros = filter_nonzeros(row)
    shifted_tiles = []
    i = 1
    while i < len(nonzeros):
        right_tile = nonzeros[i]
        left_tile = nonzeros[i - 1]
        # Try to combine the tiles at index i - 1 and i
        if left_tile == right_tile:
            # If we can merge the tiles, add a doubled tile to the result
            # and bump the index by 2 to consider the next unmerged tile
            shifted_tiles.append(left_tile + 1)
            i += 2
        else:
            # Otherwise, we cannot merge the tile at index i,
            # so we append it to the result unchanged. We bump the counter by
            # 1 to try to merge the tiles at indices i and i + 1
            shifted_tiles.append(left_tile)
            i += 1
    # If we did not merge the second to last and last tile, we have to add the
    # last tile unchanged to the result
    if i == len(nonzeros):
        shifted_tiles.append(nonzeros[-1])
    # We pad the "empty space" created by merging and shifting tiles with empty tiles
    pad_length = len(row) - len(shifted_tiles)
    return np.pad(np.array(shifted_tiles, dtype=np.int64), (0, pad_length), 'constant')

# Shifts a matrix left according to the 2048 semantics


def shift_left(matrix):
    return np.array([shift_row(row) for row in matrix])

# Shifts a matrix in a given direction according to the 2048 semantics


def shift(matrix, dir):
    # Rotate the matrix so we shift left, and then rotate back
    angle = dir.angle_to_left()
    return np.rot90(shift_left(np.rot90(matrix, angle)), -angle)


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


# Represents a 2048 board
class Board:
    def __init__(self, arg=4):
        if isinstance(arg, int):
            # initalize with side length
            self.side = arg
            self.board = create_board(self.side)
        else:
            # initialize with matrix
            self.side = len(arg)
            self.board = np.array(arg)
        self.score = 0

    def __str__(self):
        return str(np.array([[0 if i == 0 else 2 ** i for i in row] for row in self.board]))

    def score_difference(self, board):
        tiles = list(board.flatten())
        for tile in self.board.flatten():
            if tile in tiles:
                tiles.remove(tile)
        score = 0
        for tile in tiles:
            if tile != 0:
                score += 1 << tile
        return score

    # Shift this 2048 board in place
    def shift(self, dir: Dir):
        shifted = shift(self.board, dir)
        if not np.array_equiv(shifted, self.board):
            self.score += self.score_difference(shifted)
            self.board = shifted
            return True
        return False

    # True if it is possible to make another move in the game
    def can_shift(self, dir):
        return not np.array_equal(self.board, shift(self.board, dir))
    
    # Access the value of the tile at a given position
    def at(self, i, j):
        return self.board[i][j]

    # Add a new tile to a random position in the board
    # Loops if the board is full.
    def add_tile(self):
        i = random.randrange(self.side)
        j = random.randrange(self.side)
        v = 1 if random.randint(0, 1) == 0 else 2
        # Generate random points until find on that is unoccupied
        while self.at(i, j) != 0:
            i = random.randrange(self.side)
            j = random.randrange(self.side)
        # Add the tile to this unoccupied position
        self.board[i][j] = v

    def get_font(self, height, size_proportion):
        font_size = height // self.side // size_proportion
        return pygame.font.Font(None, font_size)

    def draw(self, screen, width, height):
        # font setup
        font = self.get_font(height, 2)

        tile_height = height // (self.side + 1)
        tile_width = width // (self.side + 1)
        to_shift = tile_width // 2

        for i in range(self.side):
            for j in range(self.side):
                tile_exponent = self.at(i, j)
                tileX = j * tile_width + to_shift
                tileY = i * tile_height + to_shift // 2

                tile_color = tile_colors[tile_exponent]

                text_color = white
                if tile_color == tile_2 or tile_color == tile_4:
                    text_color = gray

                tile = pygame.draw.rect(screen, tile_color, (tileX - to_shift,
                                                             tileY - to_shift // 2, tile_width, tile_height))

                tile_number = 2 ** tile_exponent
                # if no number, then text is ""]
                tile_text = font.render(str(tile_number), True,
                                        text_color) if tile_number != 1 else font.render("", True,
                                                                                         text_color)
                tile_rect = tile_text.get_rect(centerx=tileX, y=tileY)
                screen.blit(tile_text, tile_rect)

        game_status = self.end()
        if game_status[0]:
            status_text = font.render(game_status[1], True, text_color)
            status_rect = status_text.get_rect(
                centerx=width // 2, y=height - to_shift)
            screen.blit(status_text, status_rect)

        # draw vertical and horizontal separating lines
        for i in range(2):
            for j in range(self.side + 1):
                if i == 0:  # horizontal
                    pygame.draw.line(
                        screen, white, (0, j * tile_height), (tile_width * self.side, j * tile_height))
                else:  # vertical
                    pygame.draw.line(
                        screen, white, (j * tile_width, 0), (j * tile_width, tile_height * self.side))

    def end(self):
        # check if 2048 tile has been reached
        if 11 in self.board:
            return (True, "YOU WON!!")

        # check if shifting the board in any direction results in no change
        if self.can_shift(Dir.UP) or self.can_shift(Dir.DOWN) or self.can_shift(Dir.LEFT) or self.can_shift(Dir.RIGHT):
            return (False, "")
        else:
            return (True, "You Lost")
